from re import L
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Regexp, EqualTo

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

class SearchForm(FlaskForm):
    search = StringField('Find cards', validators=[
        InputRequired(),
        Regexp('^[A-Za-z- \d]{1,50}$', message='Invalid search. Please try again.')
    ])