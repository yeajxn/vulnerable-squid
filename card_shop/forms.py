from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, IntegerField, FloatField, HiddenField
from wtforms.validators import InputRequired, Regexp, EqualTo, NumberRange, Optional

"""
Using Flask-WTForms, we can provide input validation for our input fields.
The forms also come with a CSRF Token to protect against CSRF attacks.
"""

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[
        InputRequired('Please enter a username'), 
        Regexp('^[a-zA-Z0-9_]{3,15}$', message='Username must be between 3 to 15 characters long, and contain only letters, digits, _ or -')
        ])
    email = StringField('Email', validators=[
        InputRequired('Please enter your email'), 
        Regexp('^[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+$', message='Please enter a valid email')
        ])
    password = PasswordField('Password', validators=[
        InputRequired('Please enter a password'),
        Regexp('^(?=.*?[A-Z])(?=.*?[a-z]).{8,}$', message='Please enter a sufficiently complex password'),
        EqualTo('confirm', 'Passwords must match.')
        ])
    confirm = PasswordField("Re-enter Password", validators=[
        InputRequired()
        ])

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
        InputRequired('Please enter your username'), 
        Regexp('^[a-zA-Z0-9_]{3,15}$', message='Invalid username or password')
        ])
    password = PasswordField('Password', validators=[
        InputRequired(message='Please enter your password'),
        Regexp('^(?=.*?[A-Z])(?=.*?[a-z]).{8,}$', message='Invalid username or password')
    ])

class ChangePasswordForm(FlaskForm):
    current = PasswordField('Current Password', validators=[
        InputRequired('Please enter your current password'), 
        Regexp('^[a-zA-Z0-9_]{3,15}$', message='Invalid username or password')
        ])
    new = PasswordField('New Password', validators=[
        InputRequired('Please enter your new password'), 
        Regexp('^[a-zA-Z0-9_]{3,15}$', message='Invalid username or password'),
        EqualTo('confirm', 'Passwords must match')
        ])
    confirm = PasswordField('Confirm New Password')

class SearchForm(FlaskForm):
    search = StringField('Find cards', validators=[
        InputRequired(),
        Regexp('^[A-Za-z\-\ \d]{1,40}$', message='Invalid search. Please try again.')
    ])

class AddCardForm(FlaskForm):
    name = StringField('Card Name',  validators=[
        InputRequired(),
        Regexp("^[\w\-\' ]{1,40}$", message='Invalid card name')
        ])
    image = StringField('Image Link',validators=[
        InputRequired(),
        Regexp("^https\:\/\/i\.imgur\.com\/[\w]{7}\.[a-zA-Z]{3}$", message='Invalid image link')
        ])
    type = SelectField('Type', choices=[('Dark'), ('Fire'), ('Light'), ('Magic'), ('Water')], validate_choice=True)
    text = StringField('Card Text', validators=[
        InputRequired(),
        Regexp("^[\w\-\.\?\,\"\' ]{1,180}$", message='Invalid card text')
    ])
    attack = IntegerField('Attack', validators=[
        Optional(),
        NumberRange(min=0)
    ])
    hp = IntegerField('HP', validators=[
        Optional(),
        NumberRange(min=1)
    ])
    price = FloatField('Price', validators=[
        InputRequired()
    ])
    quantity=IntegerField('Quantity', validators=[
        InputRequired(),
        NumberRange(min=0)
    ])
    
class CartForm(FlaskForm):
    id = HiddenField()
    quantity = IntegerField('Quantity', validators=[
        InputRequired(),
        NumberRange(min=1)
    ])

class CartDeleteForm(FlaskForm):
    id = HiddenField()

class CartDeleteAllForm(FlaskForm):
    pass

class CheckoutForm(FlaskForm):
    pass