from .models import Users, Polls, VotePoll
from app import db
from datetime import datetime
from flask_login import current_user, login_user, logout_user, login_required
from flask import flash, request
import re

# Checks if an account has the corresponding details provided
def valid_login(username, password):
        # Check if username matches a user in the database
        user = Users.query.filter_by(username=username).first()
        if user is None:
            flash("Username does not exist. Please try again.", "error")
        
        # Check to see if the correct password, corresponding to the username, is provided
        elif user.check_password(password) == False:
            flash("Incorrect password. Please try again.", "error")
            
        else:
                return True
        return False

# Checks if the password is valid
def valid_password(password):
        if re.search(r"[a-z]+", password) and re.search(r"[A-Z]+",password) and re.search(r"[0-9]+", password) and re.search(r"[-~`!@#\$%\^&\*()\+=|,<>\?/\\\.\'\"\_]+", password):
                return True
        #flash("Invalid password provided. Please try again.")
        return False

# Checks if the given username is unique
def unique_username(username):
        user = Users.query.filter_by(username=username).first()
        # Case that the username used in creation is already taken.
        if user is not None:
            flash("Username is already taken. Please use a different one", "error")
            return False
        return True

# Checks if the given email is unique
def unique_email(email):
        user = Users.query.filter_by(email=email).first()
        if user is not None:
            flash("Email is already taken. Please use a different one", "error")
            return False
        return True

# Checks if the email is valid
def valid_email(email):
        if re.search(r"[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z0-9]+", email):
                return True
        flash("Invalid email provided. Please try again.", "error")
        return False

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
# Checks if the user submitting the vote is allowed to vote
def vote_allowed(poll_id):
        if VotePoll.query.filter_by(user_ID=current_user.user_ID, poll_ID=poll_id).first() is not None:
                flash("You have already voted.")
                return False
        elif Polls.query.get(poll_id).pollAuthor_ID == current_user.user_ID:
                flash("You cannot vote on your own polls.")
                return False
        else:
                return True

# Provides bypass message if validation fails (user tampering)
def check_validation_bypass():
        if request.method != "GET":
                flash("Form validation bypass detected. Please fill form correctly.")

# Determines if the poll results should be shown to the user
def show_results(poll):
        # If the user is logged in, checks to see if they have already voted
        if current_user.is_authenticated:
                return VotePoll.query.filter_by(user_ID = current_user.user_ID, poll_ID = poll.poll_ID).first() is not None or poll.pollAuthor_ID == current_user.user_ID
        
        # Default no vote value of None, determines if poll results are shown when page is loaded
        else:
                return False
        
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
        
        if poll.total_votes() == 0:
                bar["default"] = "background-color:black"
        return bar

# Returns a boolean for the reverse property of sort
def get_sort_order(order):
        if order == "Ascending":
                return False
        else:
                return True

# Sorts the post by the given order and mode       
def sort_by_option(option, mode, posts):
        if option == "Popularity":
                posts.sort(reverse=mode, key = lambda user_post: user_post.total_votes() )
        elif option == "Difference":
                posts.sort(reverse=mode, key = lambda user_post: abs(user_post.left_percentage() - user_post.right_percentage()))
        elif option == "Date":
                posts.sort(reverse=mode, key = lambda user_post: datetime.timestamp(user_post.creation_date))

# Checks if the option provided is within the list of allowed options   
def valid_choice(choice, choices):
        if choice in choices:
                return True
        else:
                flash("Invalid option detected. Please try again.", "error")
                return False

# Checks if a poll is allowed to be deleted
def verify_poll_deletion(poll):
        if poll is None:
                flash("Could not delete poll. poll does not exist.")
        
        elif poll.pollAuthor_ID != current_user.get_id():
                flash("You are not authorized to delete someone elses poll.")
        else:
                return True
        return False

# Checks if a comment is allowed to be deleted
def verify_comment_deletion(comment):
        if comment is None:
                flash("Could not delete comment. comment does not exist.")
        
        elif comment.user_ID != current_user.get_id():
                flash("You are not authorized to delete someone elses comment.")
        else:
                return True
        return False

# Returns list of users based on the search parameter
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
        
 # See if a given string includes another noramlised string   
def contains_string(string, search):
        string = string.lower()
        search = search.lower()
        if string.find(search) == -1:
                return False
        else:
                return True

#The following remove elements that dont match a given prompt, option or tag. Bypassed if field was left empty
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

# Checks if the username a user wants is already taken
def available_username(username):
        if not Users.query.filter_by(username=username).first() is None:
                flash("Username is already taken. Please try again")
                return False
        return True

# Checks if a given username is valid
def valid_username(username):
        if len(username) < 5:
                flash("Username must be longer than 5 characters.")
                return False
        if len(username) > 15:
                flash("Username cannot be longer than 15 characters.")
                return False
        return True

# Returns user posts that are within a certain timeframe
def get_timed_posts(choice):
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

        # Grabs the first 10 polls or less using the poll ID from each count, along with the recent vote count
        while index < 10 and index < length:
                results.append((Polls.query.get(sorted_list[index][0]), sorted_list[index][1]))
                index += 1

        return results

def test_data():
    users = []
    # Create basic test users
    for i in range(100):
        username = "user" + str(i)
        password = "Something-1" + str(i)
        email = "default" + str(i) + "@email.com"
        user = Users(username=username, email=email, password=password)

    db.session.add_all(users)
    db.session.commit()