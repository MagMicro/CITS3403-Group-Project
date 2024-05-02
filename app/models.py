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
        total_diff = 0
        total_polls = 0
        for post in self.posts():
            if post.total_votes() == 0:
                continue
            total_polls += 1
            total_votes = post.total_left() + post.total_right()
            left_percentage = post.left_percentage()
            right_percentage = post.right_percentage()
            poll_diff = abs(left_percentage - right_percentage) / 100
            total_diff += poll_diff

        if total_polls > 0:
            return round((total_diff / total_polls) * 100, 2)
        else:
            return 100
        
    def rank(self):
        users = Users.query.all()
        users.sort(key=lambda x: x.average_dif(), reverse=False)
        return users.index(self) + 1
    
    def get_ranks():
        users = Users.query.all()
        users.sort(key=lambda x: x.average_dif(), reverse=False)
        return users

class Polls(db.Model):
    __tablename__ = 'Polls'

    poll_ID = db.Column(db.Integer, primary_key=True)
    pollAuthor_ID = db.Column(db.Integer, db.ForeignKey('Users.user_ID'))
    Option1 = db.Column(db.String)
    Option2 = db.Column(db.String)
    tag1 = db.Column(db.String)
    tag2 = db.Column(db.String)
    tag3 = db.Column(db.String)
    date = db.Column(db.String)
    prompt = db.Column(db.String)
    def total_left(self):
        return VotePoll.query.filter_by(poll_ID = self.poll_ID, Vote_opt = 1).count()
    
    def total_right(self):
        return VotePoll.query.filter_by(poll_ID = self.poll_ID, Vote_opt = 2).count()

    def total_votes(self):
        return self.total_left() + self.total_right()

    def left_percentage(self):
        total_votes = self.total_votes()
        if self.total_left() != 0:
            return round((self.total_left() / total_votes) * 100, 2)
        else:
            return 0
        
    def right_percentage(self):
        total_votes = self.total_votes()
        if self.total_right() != 0:
            return round((self.total_right() / total_votes) * 100, 2)
        else:
            return 0
        
class VotePoll(db.Model):
    __tablename__ = 'VotePoll'

    user_ID = db.Column(db.Integer, db.ForeignKey('Users.user_ID'), primary_key=True)
    poll_ID = db.Column(db.Integer, db.ForeignKey('Polls.poll_ID'), primary_key=True)
    Vote_opt = db.Column(db.Integer)