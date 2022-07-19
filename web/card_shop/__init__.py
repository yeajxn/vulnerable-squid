import os
from venv import create

from flask import Flask
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

DATABASE_NAME = os.getenv('DATABASE_NAME')
DATABASE_USER = os.getenv('DATABASE_USER')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')

from .database import create_db, create_admin
create_db()
create_admin()

from . import routes