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

    posts = db.relationship('Polls', back_populates = 'author')
    votes = db.relationship('VotePoll', back_populates = 'voter')
    comments = db.relationship('Comments', back_populates = 'user')

    #Override for finding the user ID
    def get_id(self):
        return self.user_ID
    
    #Methods for getting and checking hashed password
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def wipe_account(self):
        Polls.query.filter_by(pollAuthor_ID = self.user_ID).delete()
        VotePoll.query.filter_by(user_ID = self.user_ID).delete()
        Comments.query.filter_by(user_ID = self.user_ID).delete()

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
        
    def poll_points(self, post):
        if post.total_votes() == 0:
            return 0
        poll_diff = abs(post.left_percentage() - post.right_percentage())
        return (100 - poll_diff) * post.total_votes()

    def total_points(self):
        points = 0
        for post in self.posts:
            points += self.poll_points(post)
        return points
        
    def rank(self):
        ranked = Users.get_ranks()
        return ranked[self.user_ID]

    def get_ranks():
        users = Users.query.all()
        if not users:
            return {}

        # Precompute total points to avoid multiple calculations
        user_points = {user: user.total_points() for user in users}
        
        # Sort users based on precomputed total points
        sorted_users = sorted(users, key=lambda x: user_points[x], reverse=True)
        
        ranks = {}
        rank = 1
        prev_points = user_points[sorted_users[0]]
        for user in sorted_users:
            if user_points[user] != prev_points:
                rank += 1
                prev_points = user_points[user]
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
    
    # Checks if a poll has votes or not
    def no_votes(self):
        return len(self.votes) == 0
    
    # Clears all data about a given poll
    def wipe_poll(self):
        Comments.query.filter_by(poll_ID = self.poll_ID).delete()
        VotePoll.query.filter_by(poll_ID = self.poll_ID).delete()
        db.session.delete(self)
        db.session.commit()

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
        return self.creation_date.strftime('%d/%m/%Y %-I:%M %p')

    # Functions to calcuate the proportion of votes for each given poll instance
    def total_left(self):
        return VotePoll.query.filter_by(poll_ID = self.poll_ID, Vote_opt = 1).count()
    
    def total_right(self):
        return VotePoll.query.filter_by(poll_ID = self.poll_ID, Vote_opt = 2).count()

    def total_votes(self):
        return len(self.votes)

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

    user = db.relationship('Users', back_populates = 'comments')

    def readable_date(self):
        return self.creation_date.strftime('%d/%m/%Y') + self.creation_date.strftime(' %I:%M %p').replace("0", "")
