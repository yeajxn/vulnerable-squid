import os
from dotenv import load_dotenv
load_dotenv()

from flask import Flask
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from flask_login import LoginManager
login = LoginManager(app)

from . import routes
login.login_view = "login"
login.login_message_category = "info"