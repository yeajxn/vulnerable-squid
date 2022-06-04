from distutils.log import Log
from . import app
from flask import render_template, redirect, url_for, request
from flask_login import login_manager, login_required, logout_user
from .forms import LoginForm, RegisterForm, SearchForm

@app.route("/")
def home():
    search = SearchForm()
    return render_template('home.html', title='The Card Spot - Home', search=search)

@app.route('/register', methods=['GET', 'POST'])
def register():
    search = SearchForm()
    form = RegisterForm()
    error = None    
    if form.validate_on_submit():
        error = form.username.data
    elif request.method == 'POST':
        error = next(iter(form.errors.values()))[0]
    return render_template('register.html', title='The Card Spot- Register', form=form, error=error, search=search)    

@app.route('/search')
def search():
    search = SearchForm()
    return render_template('search.html', title='The Card Spot - Search', search=search)

@app.route('/login', methods=['GET', 'POST'])
def login():
    search = SearchForm()
    form = LoginForm()
    if request.method == 'GET':
        return render_template('login.html', title='The Card Stop - Login', form=form, search=search)
    if request.method == 'POST' and form.validate_on_submit():
        return render_template('login.html', title='The Card Stop', form=form, error=form.username.data, search=search)
    else:
        error = next(iter(form.errors.values()))[0]
        return render_template('login.html', title='The Card Stop - Login', form=form, error=error, search=search)
    

@login_required
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))