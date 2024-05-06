from flask_sqlalchemy import SQLAlchemy
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from app import login
from flask_login import UserMixin

@login.user_loader
def get_user(id):
    return Users.query.get(int(id))

class Users(UserMixin, db.Model):
    __tablename__ = 'Users'

    user_ID = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String(128))
    date = db.Column(db.String(10))
    
    #Override for finding the user ID
    def get_id(self):
        return self.user_ID
    
    #Methods for getting and checking hashed password
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    #Methods for gathering user posts & their data
    def posts(self):
        return Polls.query.filter_by(pollAuthor_ID = self.user_ID)
    
    def count_posts(self):
        return self.posts().count()
    
    def average_dif(self):
        total_diff = 0
        total_polls = self.count_posts()
        for post in self.posts():
            if post.total_votes() == 0:
                continue
            poll_diff = abs(post.left_percentage() - post.right_percentage()) / 100
            total_diff += poll_diff

        if total_polls > 0:
            return round((total_diff / total_polls) * 100, 2)
        else:
            return 100
        
    def rank(self):
        ranked = Users.get_ranks()
        return ranked[self.user_ID]

    def get_ranks():
        users = Users.query.all()
        users.sort(key=lambda x: x.average_dif(), reverse=False)
        ranks = {}
        rank = 1
        prev_avg = users[0].average_dif() if users else None
        for user in users:
            if user.average_dif() != prev_avg:
                rank += 1
                prev_avg = user.average_dif()
            ranks[user.user_ID] = rank
        return ranks

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
    def to_dict(self):
        poll ={}
        poll["ID"] = self.poll_ID
        poll["Author"] = self.pollAuthor_ID
        poll["option1"] = self.Option1
        poll["option2"] = self.Option2
        poll["tag1"] = self.tag1
        poll["tag2"] = self.tag2
        poll["tag3"] = self.tag3
        poll["date"] = self.date
        poll["prompt"] = self.prompt
        poll["total"] = self.total_votes()
        poll["left%"] = self.left_percentage()
        poll["right%"] = self.right_percentage()
        return poll

    def total_left(self):
        return VotePoll.query.filter_by(poll_ID = self.poll_ID, Vote_opt = 1).count()
    
    def total_right(self):
        return VotePoll.query.filter_by(poll_ID = self.poll_ID, Vote_opt = 2).count()

    def total_votes(self):
        return self.total_left() + self.total_right()

    def left_percentage(self):
        if self.total_left() != 0:
            return round((self.total_left() / self.total_votes()) * 100, 2)
        else:
            return 0
        
    def right_percentage(self):
        if self.total_right() != 0:
            return round((self.total_right() / self.total_votes()) * 100, 2)
        else:
            return 0
        
class VotePoll(db.Model):
    __tablename__ = 'VotePoll'

    user_ID = db.Column(db.Integer, db.ForeignKey('Users.user_ID'), primary_key=True)
    poll_ID = db.Column(db.Integer, db.ForeignKey('Polls.poll_ID'), primary_key=True)
    Vote_opt = db.Column(db.Integer)