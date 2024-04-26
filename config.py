import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = "some_random_text_line"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False