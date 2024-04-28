from flask_sqlalchemy import SQLAlchemy
from app import db

class Users(db.Model):
    __tablename__ = 'Users'

    user_ID = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    date = db.Column(db.String(10))

    def count_posts(self):
        return Polls.query.filter_by(pollAuthor_ID = self.user_ID).count()

class Polls(db.Model):
    __tablename__ = 'Polls'

    poll_ID = db.Column(db.Integer, primary_key=True)
    pollAuthor_ID = db.Column(db.Integer, db.ForeignKey('Users.user_ID'))
    Option1 = db.Column(db.String)
    Option2 = db.Column(db.String)

class VotePoll(db.Model):
    __tablename__ = 'VotePoll'

    user_ID = db.Column(db.Integer, db.ForeignKey('Users.user_ID'), primary_key=True)
    poll_ID = db.Column(db.Integer, db.ForeignKey('Polls.poll_ID'), primary_key=True)
    Vote_opt = db.Column(db.Integer)