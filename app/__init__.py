from flask import Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = "some_random_text_line"
from app import routes