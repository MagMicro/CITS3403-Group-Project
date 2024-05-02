from flask_sqlalchemy import SQLAlchemy
from app import db

class Users(db.Model):
    __tablename__ = 'Users'

    user_ID = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    date = db.Column(db.String(10))

    def posts(self):
        return Polls.query.filter_by(pollAuthor_ID = self.user_ID)
    
    def count_posts(self):
        return self.posts().count()
    
    def average_dif(self):
        user_total_left = 0
        user_total_right = 0
        for post in self.posts():
            user_total_left += post.total_left()
            user_total_right += post.total_right()

        total = user_total_right + user_total_left
        if (total > 0):
            return abs(user_total_left - user_total_right)/total * 100
        else:
            return 0

class Polls(db.Model):
    __tablename__ = 'Polls'

    poll_ID = db.Column(db.Integer, primary_key=True)
    pollAuthor_ID = db.Column(db.Integer, db.ForeignKey('Users.user_ID'))
    Option1 = db.Column(db.String)
    Option2 = db.Column(db.String)
    tag1 = db.Column(db.String)
    tag2 = db.Column(db.String)
    tag3 = db.Column(db.String)
    date = db.Column(db.String(10))

    def total_left(self):
        return VotePoll.query.filter_by(poll_ID = self.poll_ID, Vote_opt = 1).count()
    
    def total_right(self):
        return VotePoll.query.filter_by(poll_ID = self.poll_ID, Vote_opt = 2).count()

class VotePoll(db.Model):
    __tablename__ = 'VotePoll'

    user_ID = db.Column(db.Integer, db.ForeignKey('Users.user_ID'), primary_key=True)
    poll_ID = db.Column(db.Integer, db.ForeignKey('Polls.poll_ID'), primary_key=True)
    Vote_opt = db.Column(db.Integer)