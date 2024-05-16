from flask_sqlalchemy import SQLAlchemy
from app import db
import datetime
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
    creation_date = db.Column(db.DateTime, default=datetime.datetime.now())
    
    # Gets all user posts
    posts = db.relationship('Polls', back_populates = 'author')
    # Gets all user votes
    votes = db.relationship('VotePoll', back_populates = 'voter')

    #Override for finding the user ID
    def get_id(self):
        return self.user_ID
    
    #Methods for getting and checking hashed password
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def voted_polls(self):
        voted_polls = []
        for vote in self.votes:
            voted_polls.append(vote.poll)
        return voted_polls
    
    def count_posts(self):
        return len(self.posts)
    
    def average_dif(self):
        total_diff = 0
        total_polls = self.count_posts()
        for post in self.posts:
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
    creation_date = db.Column(db.DateTime, default=datetime.datetime.now())
    prompt = db.Column(db.String)

    author = db.relationship('Users', back_populates = 'posts')
    votes = db.relationship('VotePoll', back_populates = 'poll')
    comments = db.relationship('Comments')
    
    #Deleted all votes associated with a given poll
    def delete_votes(self):
        votes = VotePoll.query.filter_by(poll_ID=self.poll_ID)
        for vote in votes:
            db.session.delete(vote)

    # Adds tags to Polls model instance based on how many tags it received, default is N/A
    def add_tags(self, tags):
        if len(tags) >= 1 and tags[0] != '':
            self.tag1 = tags[0]
            if len(tags) >= 2:
                self.tag2 = tags[1]
            if len(tags) == 3:
                self.tag3 = tags[2]

    # Returns the post author's username       
    def get_author(self):
        return Users.query.get(self.pollAuthor_ID).username
    
    # Creates a human readable date for a given post
    def readable_date(self):
        return self.creation_date.strftime('%d/%m/%Y') + self.creation_date.strftime(' %I:%M %p').replace("0", "")

    # Functions to calcuate the proportion of votes for each given poll instance
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
    creation_date = db.Column(db.DateTime, default=datetime.datetime.now())

    poll = db.relationship('Polls', back_populates = 'votes')
    voter = db.relationship('Users', back_populates = 'votes')

class Comments(db.Model):
    __tablename__ = 'Comments'

    comment_ID = db.Column(db.Integer, primary_key=True)
    user_ID = db.Column(db.Integer, db.ForeignKey('Users.user_ID'))
    poll_ID = db.Column(db.Integer, db.ForeignKey('Polls.poll_ID'))
    message = db.Column(db.String(500))
    creation_date = db.Column(db.DateTime, default=datetime.datetime.now())

    user = db.relationship('Users')

    def readable_date(self):
        return self.creation_date.strftime('%d/%m/%Y') + self.creation_date.strftime(' %I:%M %p').replace("0", "")
