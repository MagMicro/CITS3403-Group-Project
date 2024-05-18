from .models import Users, Polls, VotePoll
from app import db
from datetime import datetime
from flask_login import current_user, login_user, logout_user, login_required
from flask import flash, request

# Creates a new account with the provided details
def register_account(username, email, password):
        new_user = Users(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

# Create a new poll with the provided details
def create_poll(option1, option2, userID, prompt, form_tags):
        new_poll = Polls(Option1=option1, Option2=option2, pollAuthor_ID=userID, prompt=prompt)
        new_poll.add_tags(form_tags)
        db.session.add(new_poll)
        db.session.commit()

# Check if provided lists contains tags
def has_tags(tags):
        if len(tags) == 0 or tags[0] == "":
                flash("Need to use one or more tags. Please try again.", "error")
                return False
        return True

# Check that all tags submitted are valid
def valid_tags(tags, form_tags):
        for tag in form_tags:
            if tag not in tags:
                flash("Unrecognised tag/s detected. Please try again.", "error")
                return False
        return True

# Check that the options provided are diferrent
def dif_options(option1, option2):
        if option1 == option2:
                flash("Options must be different. Please try again.", "error")
                return False
        return True

# Make sure the overall post is unique
def unique_post(option1, option2):
        if (Polls.query.filter_by(Option1=option1, Option2=option2).first() is not None or Polls.query.filter_by(Option1=option2, Option2=option1).first() is not None):
                flash("Post already exists. Please try something else.", "error")
                return False
        return True

# Provides bypass message if validation fails (user tampering)
def check_validation_bypass():
        if request.method != "GET":
                flash("Form validation bypass detected. Please fill form correctly.")

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
                posts.sort(reverse=mode, key = lambda user_post: datetime.timestamp(user_post.creation_date))
        
def valid_choice(choice, choices):
        if choice in choices:
                return True
        else:
                flash("Invalid option detected. Please try again.", "error")
                return False


def verify_poll_deletion(poll):
        if poll is None:
                flash("Could not delete poll. poll does not exist.")
        
        elif poll.pollAuthor_ID != current_user.get_id():
                flash("You are not authorized to delete someone elses poll.")
        else:
                return True
        return False

def verify_comment_deletion(comment):
        if comment is None:
                flash("Could not delete comment. comment does not exist.")
        
        elif comment.user_ID != current_user.get_id():
                flash("You are not authorized to delete someone elses comment.")
        else:
                return True
        return False

def get_mode_list(mode, input, voted):
        if mode == "All":
                polls = Polls.query.all()

        elif mode == "PostID":
                polls = [Polls.query.get(int(input))]

        elif mode == "Username":
                user = Users.query.filter_by(username=input).first()
                if user is not None:
                        polls = user.posts
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

def available_username(username):
        if not Users.query.filter_by(username=username).first() is None:
                flash("Username is already taken. Please try again")
                return False
        return True

def valid_username(username):
        if len(username) < 5:
                flash("Username must be longer than 5 characters.")
                return False
        if len(username) > 15:
                flash("Username cannot be longer than 15 characters.")
                return False
        return True

def get_timed_posts(choice):
        polls = Polls.query.all()
        final = []

        # Time for daily in seconds
        time = (24*60*60)

        # Time for weekly in seconds
        if choice == "Weekly":
                time = time * 7

        # Time for monthly in seconds
        elif choice == "Monthly":
                time = time * 31


        #Important: This was a python workaround because the filter function for sql did not support datetime timestamp

        # Holds the total amount of votes for each poll that falls within the timeframe
        count_dict = {}
        votes = VotePoll.query.all()
        for vote in votes:
                # Checks if the vote happened within the required timeframe
                if(datetime.timestamp(datetime.now()) - datetime.timestamp(vote.creation_date) <= time):
                        count_dict[vote.poll_ID] = count_dict.get(vote.poll_ID, 0) + 1

        # Sorts polls based on number of votes
        sorted_list = sorted(count_dict.items(), reverse = True, key = lambda item:item[1])
        results = []

        length = len(sorted_list)
        index = 0

        # Grabs the first 10 polls or less using the poll ID from each count
        while index < 10 and index < length:
                results.append(Polls.query.get(sorted_list[index][0]))
                index += 1

        return results

