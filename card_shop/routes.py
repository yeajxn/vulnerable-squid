from functools import wraps

from . import app, db
from flask import render_template, redirect, url_for, request, flash, abort
from flask_login import login_required, login_user, logout_user, current_user
from .forms import AddCardForm, LoginForm, RegisterForm, SearchForm 
from .forms import ChangePasswordForm, CartForm, CartDeleteForm, CartDeleteAllForm, CheckoutForm
from .models import Cart, User, Card, Order, CardOrders
from .hashing import hash_password, check_hash

#Decorator function for access to admin pages
def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if current_user.is_anonymous:
            flash('Please login to continue', 'warning')
            return redirect(url_for('login'))
        if current_user.user_type != 'A':
            abort(403)
        return f(*args, **kwargs)
    return wrapper

def search_cards(search):
    cards = Card.query.filter(Card.name.like(f'%{search}%'), Card.quantity > 0).all()
    return cards

@app.route("/")
def home():
    search = SearchForm()
    return render_template('home.html', title='The Card Spot - Home', search=search)

@app.route('/cart', methods=['GET', 'POST'])
@login_required
def cart():
    search=SearchForm()
    form = CartForm()
    checkout = CheckoutForm()
    clear_cart = CartDeleteAllForm()
    if form.validate_on_submit():
        cardID = form.id.data
        quantity = form.quantity.data

        cart_item = Cart.query.filter(Cart.userID==current_user.userID, Cart.cardID==cardID).first()
        if cart_item:
            cart_item.quantity += int(quantity)
            db.session.commit()
            flash('Cart quantity updated', 'success')
        else:
            cart_item = Cart(userID=current_user.userID, cardID=cardID, quantity=quantity)
            db.session.add(cart_item)
            db.session.commit()
            flash('Item added to card', 'success')
    elif request.method == 'POST':
        flash('Something went wrong', 'warning')
        return redirect(url_for('search'))
        
    cart = current_user.cart
    print(cart)
    total = 0
    cart_delete_forms = []
    for item in cart:
        total += item.cardInfo.price * item.quantity
        cart_delete_form = CartDeleteForm()
        cart_delete_form.id.data = item.cardID
        cart_delete_forms.append(cart_delete_form)
    return render_template('cart.html', cart=cart, search=search, total=total, 
    cart_delete_forms=cart_delete_forms, checkout=checkout, clear_cart=clear_cart, title='The Card Spot - Cart')

@app.route('/cart/delete', methods=['POST'])
@login_required
def cart_delete():
    form = CartDeleteForm()
    if form.validate_on_submit():
        item = Cart.query.filter(Cart.userID==current_user.userID, Cart.cardID==form.id.data).first()
        if item:
            db.session.delete(item)
            db.session.commit()
            flash('Item removed from cart', 'success')
        else:
            flash('Something went wrong, unable to remove cart item', 'danger')
    return redirect(url_for('cart'))

@app.route('/cart/delete-all', methods=['POST'])
@login_required
def cart_delete_all():
    form = CartDeleteAllForm()
    if form.validate_on_submit():
        check = Cart.query.filter_by(userID = current_user.userID)
        if check.first():
            check.delete()
            db.session.commit()
            flash('Emptied cart', 'success')
        else:
            flash('Nothing in cart', 'info')
    return redirect(url_for('cart'))

@app.route('/checkout', methods=['POST'])
@login_required
def checkout():
    form = CheckoutForm()
    if form.validate_on_submit():
        users_cart = Cart.query.filter_by(userID = current_user.userID)
        if users_cart.first():
            
            #create new order
            new_order = Order(userID=current_user.userID, total=0)
            db.session.add(new_order)
            db.session.commit()
            
            #Add to CardOrders
            total = 0

            #Check stock
            for item in users_cart.all():
                card = Card.query.get(item.cardID)
                card_quantity = card.quantity
                if card_quantity < item.quantity:
                    flash(f'Unable to purchase {card.name}. Check if there is stock available from the card listing.', 'warning')
                    db.session.delete(new_order)
                    db.session.commit()
                    return redirect(url_for('cart'))
                total += card.price * item.quantity
                card.quantity -= item.quantity
                card_order = CardOrders(cardID=item.cardID, orderID=new_order.orderID, unit_price=card.price, quantity=item.quantity)
                db.session.add(card_order)

            new_order.total = total

            #delete from cart
            users_cart.delete()

            #Commit all changes
            db.session.commit()
            flash('Purchase successful!', 'success')     

        else:
            flash('Your cart is empty', 'info')
    else:        
        flash('Something went wrong....', 'danger')
    return redirect(url_for('cart'))


@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    search = SearchForm()
    if form.validate_on_submit():
        if check_hash(current_user.password, form.current.data):
            hash = hash_password(form.new.data)
            current_user.password = hash
            db.session.commit()
            flash('Password changed', 'success')
        else:
            flash('Unable to change password. Check your current password', 'danger')
    elif request.method == 'POST':
        flash(next(iter(form.errors.values()))[0], 'danger')
    return render_template('changePassword.html', search=search, form=form, title='Change Password')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    search = SearchForm()
    form = LoginForm()
    
    if request.method == 'POST':
        if form.validate_on_submit():
            identifier = form.username.data.lower()
            user = User.query.filter((User.username==identifier)|(User.email==identifier)).first()
            if user and check_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('home'))
            else:
                flash('Invalid username or password', 'danger')
        else:
            error = next(iter(form.errors.values()))[0]
            flash(error, 'danger')

    return render_template('login.html', title='The Card Spot - Login', form=form, search=search)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('User logged out', 'success')
    return redirect(url_for('login'))


@app.route('/manage', methods=['GET', 'POST'])
@admin_required
def manage():
    searchForm = SearchForm()
    if searchForm.validate_on_submit():
        cards = search_cards(searchForm.search.data)
    elif request.method=='GET':
        cards = Card.query.all()
    else:
        flash(f'Invalid search: {searchForm.search.data}', 'info')
        cards=None
    return render_template('manageCards.html', search=searchForm, cards=cards, title='Manage Shop')

@app.route('/manage/add_card', methods=['GET', 'POST'])
@admin_required
def manage_add_card():
    search = SearchForm()
    form = AddCardForm()
    buttontext = "Add"
    headertext = 'Add New Card'
    if form.validate_on_submit():
        name = form.name.data
        image = form.image.data
        type = form.type.data
        text = form.text.data
        hp = int(form.hp.data) if form.hp.data else None
        attack = int(form.attack.data) if form.attack.data else None
        price = float(form.price.data)
        quantity = int(form.quantity.data) if form.quantity.data else 0
        new_card = Card(name=name, image=image, type=type, text=text, hp=hp, attack=attack, price=price, quantity=quantity)
        db.session.add(new_card)
        db.session.commit()
        flash(f'{name} Added', 'success')
        return redirect(url_for('manage'))
    elif request.method == 'POST':
        flash(next(iter(form.errors.values()))[0], 'warning')
    return render_template('card.html', search=search, form=form, buttontext=buttontext, headertext=headertext, title='Manage Shop - Add Card')

@app.route('/manage/edit/<id>', methods=['GET', 'POST'])
@admin_required
def manage_edit_card(id):
    search = SearchForm()
    card = Card.query.get(id)
    if card:
        form = AddCardForm(obj=card)
        if form.validate_on_submit():
            card.name = form.name.data
            card.image = form.image.data
            card.type = form.type.data
            card.text = form.text.data
            card.hp = int(form.hp.data) if form.hp.data else None
            card.attack = int(form.attack.data) if form.attack.data else None
            card.price = float(form.price.data)
            card.quantity = int(form.quantity.data) if form.quantity.data else 0
            db.session.commit()
            flash('Card edited', 'success')
        elif request.method == 'POST':
            flash(next(iter(form.errors.values()))[0], 'warning')
        buttontext = 'Confirm'
        headertext = f'Edit {card.name}'
        return render_template('card.html', search=search, form=form, headertext=headertext, buttontext=buttontext, 
        title='Manage Shop - Edit Card')
    flash('Something went wrong', 'danger')
    return redirect(url_for('manage'))

@app.route('/orders')
def orders():
    search= SearchForm()
    orders = Order.query.filter_by(userID=current_user.userID)
    return render_template('orders.html', search=search, orders=orders.all(), title='The Card Spot - Orders')

@app.route('/register', methods=['GET', 'POST'])
def register():
    search = SearchForm()
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data.lower()
        hash = hash_password(form.password.data)
        email = form.email.data.lower()
        exists = User.query.filter((User.username==username)|(User.email==email)).first()
        if exists:
            flash('Username or email already in use', 'warning')
        else:
            new_user = User(username=username,password=hash, email=email)
            db.session.add(new_user)
            db.session.commit()
            flash('User successfully registered!', 'success')

    elif request.method == 'POST':
        flash(next(iter(form.errors.values()))[0], 'danger')

    return render_template('register.html', title='The Card Spot- Register', form=form, search=search)    

@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    search = SearchForm()
    if search.validate_on_submit():
        cards = search_cards(search.search.data)
    elif request.method == 'GET':
        cards = Card.query.filter(Card.quantity > 0).all()
    else:
        flash('Invalid search', 'warning')
        return render_template('search.html', title='The Card Spot - Search', search=search)

    forms = []
    for card in cards:
        form = CartForm()
        form.id.data = card.cardID
        forms.append(form)    
    return render_template('search.html', title='The Card Spot - Search', search=search, cards=cards, forms=forms)