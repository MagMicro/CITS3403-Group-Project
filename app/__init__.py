from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
app = Flask(__name__)
app.config['SECRET_KEY'] = "some_random_text_line"
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'static', 'database.db')
db = SQLAlchemy(app)

from app import routes