from functools import wraps
from . import app
from flask import render_template, redirect, url_for, request, flash, make_response
from .forms import AddCardForm, LoginForm, RegisterForm, SearchForm 
from .forms import ChangePasswordForm, CartForm, CartDeleteForm, CartDeleteAllForm, CheckoutForm
from .database import create_card_orders, getUser, get_card, get_cards, get_cart, get_cart_item, get_order, get_orders
from .database import create_user, create_card, add_to_cart, create_order, check_login
from .database import delete_cart_item, delete_cart
from datetime import datetime

def logged_in(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not request.cookies.get('logged_in'):
            flash('Login required', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return wrapper

def admin_user(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if request.cookies.get('user_type') == 'A':
            return f(*args, **kwargs)
        return redirect(url_for('home'))
    return wrapper

@app.route("/")
def home():
    search = SearchForm()
    return render_template('home.html', title='The Card Spot - Home', search=search)

@app.route('/cart', methods=['GET', 'POST'])
@logged_in
def cart():
    search=SearchForm()
    form = CartForm()
    checkout = CheckoutForm()
    clear_cart = CartDeleteAllForm()
    if form.validate_on_submit():
        cardID = int(form.id.data)
        quantity = form.quantity.data
        cart_item = get_cart_item(request.cookies.get('userID'), form.id.data)
        if cart_item:
            cart_item.quantity += int(quantity)
            flash('Cart quantity updated', 'success')
        else:
            add_to_cart(cardID, request.cookies.get('userID'), quantity)
            flash('Item added to card', 'success')

    elif request.method == 'POST':
        flash('Something went wrong', 'warning')
        return redirect(url_for('search'))
        
    cart = get_cart(request.cookies.get('userID'))
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
@logged_in
def cart_delete():
    form = CartDeleteForm()
    if form.validate_on_submit():
        delete_cart_item(request.cookies.get('userID'), form.id.data)
        flash('Item removed from cart', 'success')
    else:
        flash('Something went wrong, unable to remove cart item', 'danger')
    return redirect(url_for('cart'))

@app.route('/cart/delete-all', methods=['POST'])
@logged_in
def cart_delete_all():
    form = CartDeleteAllForm()
    if form.validate_on_submit():
        delete_cart(request.cookies.get('userID'))
        flash('Emptied cart', 'success')
    else:
        flash('Nothing in cart', 'info')
    return redirect(url_for('cart'))

@app.route('/checkout', methods=['POST'])
@logged_in
def checkout():
    form = CheckoutForm()
    if form.validate_on_submit():
        users_cart = get_cart(request.cookies.get('userID'))
        if users_cart:
            cards = []
            for item in users_cart:
                card = get_card(item.cardID)
                cards.append(card)
                if card.quantity < item.quantity:
                    flash(f'Unable to purchase {card.name}. Check if there is stock available from the card listing.', 'warning')
                    return redirect(url_for('cart'))
            #create new order
            new_order = create_order(request.cookies.get('userID'))
            #Add to CardOrders
            total = 0
            #Check stock
            for i, card in enumerate(cards):  
                total += card.price * users_cart[i].quantity
                card.quantity = card.quantity - users_cart[i].quantity
                create_card_orders(cardID=item.cardID, orderID=new_order, unit_price=card.price, quantity=users_cart[i].quantity)
            new_order = get_order(new_order)
            new_order.total = total

            #delete from cart
            delete_cart(request.cookies.get('userID'))

            flash('Purchase successful!', 'success')     

        else:
            flash('Your cart is empty', 'info')
    else:        
        flash('Something went wrong....', 'danger')
    return redirect(url_for('cart'))


@app.route('/change_password', methods=['GET', 'POST'])
@logged_in
def change_password():
    form = ChangePasswordForm()
    search = SearchForm()
    if form.validate_on_submit():
        new = form.new.data
        current = form.current.data
        user = getUser(userID=int(request.cookies.get('userID')))
        if user:
            if user.password == current:   
                user.password = new
                flash('Password changed', 'success')
            else:
                flash('Invalid password', 'warning')
        else:
            flash('Uh oh something went wrong', 'danger ')
    elif request.method == 'POST':
        flash(next(iter(form.errors.values()))[0], 'danger')
    return render_template('changePassword.html', search=search, form=form, title='Change Password')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.cookies.get('logged_in'):
        return redirect(url_for('home'))
    search = SearchForm()
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.username.data.lower()
            password = form.password.data
            #Returns User object if username and password is correct
            user = check_login(username, password)
            if user:
                resp = make_response(redirect(url_for('home')))
                resp.set_cookie('logged_in', '1')
                resp.set_cookie('userID', str(user.userID))
                resp.set_cookie('username', str(user.username))
                return resp
            else:
                flash('Invalid username or password', 'danger')
        else:
            error = next(iter(form.errors.values()))[0]
            flash(error, 'danger')

    return render_template('login.html', title='The Card Spot - Login', form=form, search=search)

@app.route('/logout')
@logged_in
def logout():
    resp = make_response(redirect(url_for('login')))
    for cookie in request.cookies:
        resp.delete_cookie(cookie)
    flash('User logged out', 'success')
    return resp

@app.route('/manage', methods=['GET', 'POST'])
@logged_in
@admin_user
def manage():
    searchForm = SearchForm()
    if searchForm.validate_on_submit():
        cards = get_cards(request.form['search'])
    elif request.method=='GET':
        cards = get_cards()
    else:
        flash(f'Invalid search: {searchForm.search.data}', 'info')
        cards=None
    return render_template('manageCards.html', search=searchForm, cards=cards, title='Manage Shop')

@app.route('/manage/add_card', methods=['GET', 'POST'])
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
        new_card = create_card(name=name, image=image, type=type, text=text, hp=hp, attack=attack, price=price, quantity=quantity)
        flash(f'{new_card.name} Added', 'success')
        return redirect(url_for('manage'))
    elif request.method == 'POST':
        flash(next(iter(form.errors.values()))[0], 'warning')
    return render_template('card.html', search=search, form=form, buttontext=buttontext, headertext=headertext, title='Manage Shop - Add Card')

@app.route('/manage/edit/<id>', methods=['GET', 'POST'])
def manage_edit_card(id):
    search = SearchForm()
    card = get_card(int(id))
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
@logged_in
def orders():
    search= SearchForm()
    orders = get_orders(userID=request.cookies['userID'])
    return render_template('orders.html', search=search, orders=orders, title='The Card Spot - Orders')

@app.route('/register', methods=['GET', 'POST'])
def register():
    search = SearchForm()
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data.lower()
        email = form.email.data.lower()
        exists = getUser(username=username, email=email)

        if exists:
            flash('Username or email already in use', 'warning')
        else:
            user = create_user(username=username,password=form.password.data, email=email)
            flash(f'{user.username} successfully registered!', 'success')

    elif request.method == 'POST':
        flash(next(iter(form.errors.values()))[0], 'danger')
    return render_template('register.html', title='The Card Spot- Register', form=form, search=search)    

@app.route('/search', methods=['GET', 'POST'])
def search():
    search = SearchForm()
    s = request.values.get('search')
    if s:
        cards = get_cards(s)
    else:
        cards = get_cards()


    forms = []
    for card in cards:
        form = CartForm()
        print(card)
        form.id.data = card.cardID
        forms.append(form)    
    return render_template('search.html', title='The Card Spot - Search', search=search, cards=cards, forms=forms, searchterm=s)