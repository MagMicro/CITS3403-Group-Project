from .models import Users, Polls, VotePoll
from app import db
from flask import render_template, redirect, url_for, flash
from datetime import date, datetime

# Initialises the display values for a given polls vote percentage bar
def bar_init(poll):
        bar = {}
        bar["left"] = "width:" + str(poll.left_percentage()) + "%"
        bar["right"] = "width:" + str(poll.right_percentage()) + "%"
        bar["divider"] = "left:" + str(poll.left_percentage() - 0.5) + "%"
        if poll.left_percentage() == 0 or poll.left_percentage() == 100:
                bar["ShowDivider"] = False
        else:
                bar["ShowDivider"] = True
        return bar

def get_sort_order(order):
        if order == "Ascending":
                return False
        else:
                return True
        
def sort_by_option(option, mode, posts):
        if option == "Popularity":
                posts.sort(reverse=mode, key = lambda user_post: user_post.total_votes() )
        elif option == "Difference":
                posts.sort(reverse=mode, key = lambda user_post: abs(user_post.left_percentage() - user_post.right_percentage()))
        elif option == "Date":
                posts.sort(reverse=mode, key = lambda user_post: datetime.timestamp(datetime.strptime(user_post.date, "%d/%m/%Y %H:%M:%S")))
        
def valid_choice(choice, choices):
        if choice in choices:
                return True
        else:
                return False

def get_mode_list(mode, input):
        if mode == "All":
                return Polls.query.all()

        elif mode == "PostID":
                return [Polls.query.get(int(input))]

        elif mode == "Username":
                user = Users.query.filter_by(username=input).first()
                if user is not None:
                        return user.posts()
                else:
                        return []