from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, IntegerField, FloatField, HiddenField
from wtforms.validators import InputRequired, EqualTo, NumberRange, Optional

"""
Using Flask-WTForms, we can provide input validation for our input fields.
The forms also come with a CSRF Token to protect against CSRF attacks.
"""

class RegisterForm(FlaskForm):
    class Meta:
        csrf = False
    username = StringField('Username', validators=[
        InputRequired('Please enter a username'), 
        ])
    email = StringField('Email', validators=[
        InputRequired('Please enter your email'), 
        ])
    password = PasswordField('Password', validators=[
        InputRequired('Please enter a password'),
        EqualTo('confirm', 'Passwords must match.')
        ])
    confirm = PasswordField("Re-enter Password", validators=[
        InputRequired()
        ])

class LoginForm(FlaskForm):
    class Meta:
        csrf = False
    username = StringField('Username', validators=[
        InputRequired('Please enter your username'), 
        ])
    password = PasswordField('Password', validators=[
        InputRequired(message='Please enter your password'),
        ])

class ChangePasswordForm(FlaskForm):
    class Meta:
        csrf = False
    current = PasswordField('Current Password', validators=[
        InputRequired('Please enter your current password'), 
        ])
    new = PasswordField('New Password', validators=[
        InputRequired('Please enter your new password'), 
        EqualTo('confirm', 'Passwords must match')
        ])
    confirm = PasswordField('Confirm New Password')

class SearchForm(FlaskForm):
    class Meta:
        csrf = False
    search = StringField('Find cards', validators=[
        InputRequired(),
        ])

class AddCardForm(FlaskForm):
    class Meta:
        csrf = False
    name = StringField('Card Name',  validators=[
        InputRequired(),
        ])
    image = StringField('Image Link',validators=[
        InputRequired(),
        ])
    type = SelectField('Type', choices=[('Dark'), ('Fire'), ('Light'), ('Magic'), ('Water')], validate_choice=True)
    text = StringField('Card Text', validators=[
        InputRequired(),
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
    class Meta:
        csrf = False
    id = HiddenField()
    quantity = IntegerField('Quantity', validators=[
        InputRequired(),
        NumberRange(min=1)
    ])

class CartDeleteForm(FlaskForm):
    class Meta:
        csrf = False
    id = HiddenField()

class CartDeleteAllForm(FlaskForm):
    class Meta:
        csrf = False

class CheckoutForm(FlaskForm):
    class Meta:
        csrf = False

class ResetDatabaseForm(FlaskForm):
    class Meta:
        csrf = True