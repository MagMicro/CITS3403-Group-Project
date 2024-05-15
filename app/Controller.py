from .models import Users, Polls, VotePoll
from app import db
from datetime import datetime
from flask_login import current_user, login_user, logout_user, login_required

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

def get_mode_list(mode, input, voted):
        if mode == "All":
                polls = Polls.query.all()

        elif mode == "PostID":
                polls = [Polls.query.get(int(input))]

        elif mode == "Username":
                user = Users.query.filter_by(username=input).first()
                if user is not None:
                        polls = user.posts()
                else:
                        return []
                
        # Both means no further filtering is required
        if voted == "Both":
                return polls
        
        polls = set(polls)
        # Gets the voted polls from the user, empty if they arent logged in
        if current_user.is_authenticated:
                voted_polls = set(current_user.voted_polls())
        else:
                voted_polls = set()

        # Return only posts the user has voted on
        if voted == "Yes":
                return list(polls.intersection(voted_polls))
        # Return only the posts that have not been voted on by the user
        elif voted == "No":
                return list(polls.difference(voted_polls))
        
def contains_string(string, search):
        string = string.lower()
        search = search.lower()
        if string.find(search) == -1:
                return False
        else:
                return True
        
def filter_by_prompt(prompt, posts):
        if prompt != "":
                final = []
                for post in posts:
                        if contains_string(post.prompt, prompt):
                                final.append(post)
                return final
        return posts

def filter_by_choice(choice, posts):
        if choice != "":
                final = []
                for post in posts:
                        if contains_string(post.Option1, choice) or contains_string(post.Option2, choice):
                                final.append(post)
                return final
        return posts

def filter_by_tag(tag, posts):
        if tag != "":
                final = []
                for post in posts:
                        if post.tag1 == tag or post.tag2 == tag or post.tag3 == tag:
                                final.append(post)
                return final
        return posts