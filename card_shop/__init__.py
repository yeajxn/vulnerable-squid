import os
from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

from . import routes