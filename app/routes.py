from app import app
from flask import request, render_template, g, session, redirect, url_for, jsonify, abort, flash
from app.forms import *
from .models import Users, Polls, VotePoll, Comments
from app import db
from datetime import date, datetime

from app.Controller import *
import random


from flask_login import current_user, login_user, logout_user, login_required

@app.route('/')
def home():
    return render_template('home.html', search=PollSearch(), title="Home")

@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        print(f"User attempted login with username: {username}, password: {password}")

        # Check if username matches a user in the database
        user = Users.query.filter_by(username=username).first()
        if user is None:
            flash("Username does not exist. Please try again.", "error")
            return render_template('loginPage.html', search=PollSearch(), form=form)
        
        elif user.check_password(password) == False:
            flash("Invalid password. Please try again.", "error")
            return render_template('loginPage.html', search=PollSearch(), form=form)
        
        else:
            flash("Login Successful: Welcome " + user.username)
            login_user(user, remember = form.remember.data)
            return redirect(url_for('home'))

    print("User accessed the login page")
    return render_template('loginPage.html', search=PollSearch(), form=form, title="Login")

@app.route('/create_account', methods=['POST', 'GET'])
def create_account():
    form = CreationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        print(f"User attempting account creation with username: {username}, email: {email}, password: {password}")

        user = Users.query.filter_by(username=username).first()
        if user is not None:
            flash("Username is already taken.", "error")
            return render_template('accountCreationPage.html', search=PollSearch(), form=form, title = "Account Creation")

        user = Users.query.filter_by(email=email).first()
        if user is not None:
            flash("Email is already taken.", "error")
            return render_template('accountCreationPage.html', search=PollSearch(), form=form, title = "Account Creation")

        new_user = Users(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        print("Account created")
        form = LoginForm()
        flash("Account created successfully.")
        return render_template('loginPage.html', search=PollSearch(), form=form, title = "Login")

    print("User accessed the Account Creation page")
    return render_template('accountCreationPage.html', search=PollSearch(), form=form, title="Account Creation")

@app.route('/account', methods=['POST', 'GET'])
def account():
    if current_user.is_anonymous:
        return redirect(url_for('login'))
    else:
        user = Users.query.filter_by(user_ID=current_user.user_ID).first()
        notification = render_template("Notification.html", item = "post")
        return render_template('account.html', search=PollSearch(), title = "account",  user=user, deletion=AccountDeletion(), filter=AccountPostFilter(), form=AccountUsername(), notification = notification)

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html', search=PollSearch(), title="About")

@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/popular', methods=['GET'])
def popular():
    return render_template('popular.html', search=PollSearch(), title="Popular")

@app.route('/ranking', methods=['GET'])
def ranking():
    if current_user.is_anonymous:
        return redirect(url_for('login'))
    else:
        user = Users.query.filter_by(user_ID=current_user.user_ID).first()
        ranked = Users.get_ranks()
        rank_data = []
        for i in range(min(10, len(ranked.keys()))):
            key = list(ranked.keys())[i]
            user_rank = {
                'username': Users.query.filter_by(user_ID=key).first().username,
                'rank': ranked[key],
                'average': Users.query.filter_by(user_ID=key).first().average_dif(),
                'posts': Users.query.filter_by(user_ID=key).first().count_posts()
            }
            rank_data.append(user_rank)
            
        return render_template('ranking.html', search=PollSearch(), title="Ranking", user=user, rank_data=rank_data)

@app.route('/create', methods=['POST', 'GET'])
def create():
    if current_user.is_anonymous:
        return redirect(url_for('login'))
    
    tags = PollSearch().tags
    form = PollForm()
    PollBar = render_template('PollBar.html')

    if form.validate_on_submit():
        userID = current_user.user_ID
        prompt = form.prompt.data.capitalize()
        option1 = form.option1.data.capitalize()
        option2 = form.option2.data.capitalize()
        form_tags = form.tags.data.split(',')

        #Check that a valid prompt, and associated options are present
        if prompt == "" or option1 == "" or option2 == "":
                flash("Please make sure to fill in every field.", "error")
                return render_template('create.html', search=PollSearch(), form=form, title = "Create", tags=tags, PollBar=PollBar)
        
        #Make sure all submitted tags are valid
        for tag in form_tags:
            if tag == "":
                flash("Need to use one or more tags. Please try again.", "error")
                return render_template('create.html', search=PollSearch(), form=form, title = "Create", tags=tags, PollBar=PollBar)
            if tag not in tags:
                flash("Unrecognised tag/s detected. Please try again.", "error")
                return render_template('create.html', search=PollSearch(), form=form, title = "Create", tags=tags, PollBar=PollBar)
        if option1 == option2:
            flash("Options must be different. Please try again.", "error")
            return render_template('create.html', search=PollSearch(), form=form, title = "Create", tags=tags, PollBar=PollBar)
        #Make sure the post is unique
        if (Polls.query.filter_by(Option1=option1, Option2=option2).first() is not None or Polls.query.filter_by(Option1=option2, Option2=option1).first() is not None):
            flash("Post already exists. Please try something else.", "error")
            return render_template('create.html', search=PollSearch(), form=form, title = "Create", tags=tags, PollBar=PollBar)

        print(f"User attempting to create a poll with options:{prompt}, {option1}, {option2} and tags: {form_tags}")
        
        #Create new poll object
        new_poll = Polls(Option1=option1, Option2=option2, pollAuthor_ID=userID, prompt=prompt)
        new_poll.add_tags(form_tags)

        db.session.add(new_poll)
        db.session.commit()
        print("Poll created")
        flash("Poll has been created successfully.")
        return redirect(url_for('home'))
    print("User accessed the create page")
    return render_template('create.html', search=PollSearch(), form=form, title="Create", tags=tags, PollBar=PollBar)

@app.route('/GetUserPosts/<option>/<order>', methods=["GET"])
def generate_posts(option, order):
    posts = current_user.posts

    if valid_choice(order, AccountPostFilter().SortOrder.choices):
        mode = get_sort_order(order)
    else:
        flash("Invalid sort order detected. Please try again.", "error")
        return redirect(url_for("account"))

    if valid_choice(option, AccountPostFilter().SortOption.choices):
        sort_by_option(option, mode, posts)
    else:
        flash("Invalid sort option detected. Please try again.", "error")
        return redirect(url_for("account"))
        
    return render_template("UserPosts.html", search=PollSearch(), posts = posts, url = url_for("home"))

@app.route('/DeletePost/<int:id>', methods = ['GET'])
@login_required
def delete_user_post(id):
    deleted_post = Polls.query.get(id)

    if deleted_post is None:
        flash("Could not delete post. Post does not exist.")
        
    elif deleted_post.pollAuthor_ID != current_user.get_id():
        flash("You are not authorized to delete someone elses post.")

    else:
        deleted_post.wipe_poll()
        db.session.delete(deleted_post)
        db.session.commit()
        flash("Post was successfully deleted.")
        return url_for("account")

@app.route('/DeleteComment/<int:id>', methods = ['GET'])
@login_required
def delete_user_comment(id):
    deleted_comment = Comments.query.get(id)
    poll_id = deleted_comment.poll_ID

    if deleted_comment is None:
        flash("Could not delete post. Post does not exist.")
        
    elif deleted_comment.user_ID != current_user.get_id():
        flash("You are not authorized to delete someone elses comment.")

    else:
        db.session.delete(deleted_comment)
        db.session.commit()
        flash("Comment was successfully deleted.")
        return url_for('get_post', poll_id=int(poll_id))

@app.route("/DeleteAccount", methods = ["POST"])
@login_required
def delete_account():
    form = AccountDeletion()
    if(form.validate_on_submit()):
        password = form.password.data

        #Verify the password provided
        if(current_user.check_password(password)):
            #Delete all content associated with a user and their posts
            current_user.wipe_account()
    
            current = Users.query.get(current_user.user_ID)
            logout_user()

            db.session.delete(current)
            db.session.commit()
            flash("Account Successfully Deleted.")
            return redirect(url_for("login"))
        
        #Incorrect password provided
        else:
            flash("Invalid password. Please try again", "error")
            return redirect(url_for("account"))
        
    flash("Something went wrong. Please try again", "error")
    return redirect(url_for("account"))

@app.route('/random', methods=['GET'])
def get_random_poll():
    return redirect

@app.route('/api/poll/random', methods=['GET'])
def random_poll():
    notification = render_template("Notification.html", item = "comment")
    if current_user.is_anonymous:
        available_polls = Polls.query.all()
        random_poll = random.choice(available_polls)
        PollBar = render_template('PollBar.html', bar = bar_init(random_poll))
        return render_template('RandomPoll.html', poll = random_poll, search=PollSearch(), PollBar = PollBar, comment=CommentForm(), notification = notification), 200

    else:
        voted_polls = [vote.poll_ID for vote in VotePoll.query.filter_by(user_ID=current_user.user_ID).all()]
        available_polls = Polls.query.filter(Polls.poll_ID.notin_(voted_polls)).filter(Polls.pollAuthor_ID.notin_([current_user.user_ID])).all()

        if not available_polls:
            flash("No more random polls available. Please try again later.")
            return redirect(url_for("home"))

        random_poll = random.choice(available_polls)
        PollBar = render_template('PollBar.html', bar = bar_init(random_poll))
        notification = render_template("Notification.html", item = "comment")
        return render_template('RandomPoll.html', submission=PollSubmissionForm(), poll = random_poll, search=PollSearch(), PollBar = PollBar, comment=CommentForm(), notification = notification), 200

@app.route('/api/poll/vote', methods=['POST'])
def cast_vote():
    # redirect anonymous users to the login page
    if current_user.is_anonymous:
        flash("You need to log in to vote.")
        return url_for("login"), 404
    
    data = request.get_json()
    poll_id = data.get('poll_id')
    option = data.get('option')

    # Invalid options are sent to the server.
    if not poll_id or option not in ['1', '2']:
        flash("Invalid voting option detected. Please try again.")
        return "", 400

    # User cannot vote on the same post
    user_vote = VotePoll.query.filter_by(user_ID=current_user.user_ID, poll_ID=poll_id).first()
    if user_vote is not None:
        flash("You have already voted.")
        return "", 403

    new_vote = VotePoll(user_ID=current_user.user_ID, poll_ID=poll_id, Vote_opt=int(option))
    db.session.add(new_vote)
    db.session.commit()
    return "", 200

@app.route('/Poll/<int:poll_id>', methods=['GET', 'POST'])
def get_post(poll_id):
    poll = Polls.query.get(poll_id)
    # Case that the user attempts to look for a pollID that currently doesnt exist
    if(poll is None):
        flash("Poll does not exist.")
        return redirect(url_for('home'))
    
    # If the user is logged in, checks to see if they have already voted
    if current_user.is_authenticated:
        vote = VotePoll.query.filter_by(user_ID = current_user.user_ID, poll_ID = poll.poll_ID).first()
        print(vote)
    # Default no vote value of None, determines if poll results are shown when page is loaded
    else:
        vote = None

    PollBar = render_template('PollBar.html', bar = bar_init(poll))
    notification = render_template("Notification.html", item = "comment")
    return render_template("IndividualPost.html", search=PollSearch() , submission=PollSubmissionForm(), poll=poll, vote=vote, PollBar = PollBar, comment=CommentForm(), notification = notification), 200
    
@app.route('/SearchOptions', methods=['POST'])
def search_results():
    form = PollSearch()

    # Initialise variables for form data
    input = form.SearchBar.data
    mode = form.SearchMode.data
    voted = form.Voted.data
    prompt = form.SearchPrompt.data
    choice1 = form.SearchChoice1.data
    choice2 = form.SearchChoice2.data
    tag1 = form.Tag1.data
    tag2 = form.Tag2.data
    tag3 = form.Tag3.data
    option = form.SearchOption.data
    order = form.SearchOrder.data

    # Validate the search mode used
    if valid_choice(mode, form.SearchMode.choices) and valid_choice(voted, form.Voted.choices):
        # Return a list with posts found via form input, mode & vote status
        posts = get_mode_list(mode, input, voted)
    else:
        # Invalid search mode was submitted
        flash("Invalid mode detected. Please try again.")
        return redirect(url_for("home"))

    # Returns posts whose prompt/choices contain a certain string (if the fields weren't empty)
    posts = filter_by_prompt(prompt, posts)
    posts = filter_by_choice(choice1, posts)
    posts = filter_by_choice(choice2, posts)
    posts = filter_by_tag(tag1, posts)
    posts = filter_by_tag(tag2, posts)
    posts = filter_by_tag(tag3, posts)

    # Validate the sort order
    if valid_choice(order, PollSearch().SearchOrder.choices):
        # get which order to sort the posts by (Ascending / Descending)
        mode = get_sort_order(order)
    else:
        # Invalid filter order was submitted
        flash("Invalid sort order detected. Please try again.", "error")
        return redirect(url_for("home"))

    # Validate the sort option (what to sort by)
    if valid_choice(option, PollSearch().SearchOption.choices):
        # Sort the list using the previously calculated order and the search option
        sort_by_option(option, mode, posts)
    else:
        # Invalid filter option was submitted
        flash("Invalid sort option detected. Please try again.", "error")
        return redirect(url_for("home"))

    return render_template("SearchResults.html", search=PollSearch(), posts=posts)

@app.route('/ChangeUsername', methods = ['POST'])
@login_required
def change_username():
    form = AccountUsername()
    if form.validate_on_submit():
        id = form.AccountID.data
        username = form.AccountUsername.data
        if current_user.is_authenticated and current_user.user_ID == id:
            if not valid_username(username) or not available_username(username):
                return redirect(url_for('account'))
            
            user = Users.query.get(id)
            user.username = username
            db.session.add(user)
            db.session.commit()
            flash("Username was successfully changed.")
            return redirect(url_for('account'))

    flash("You do not have permission to do this.")
    return redirect(url_for('account'))

@app.route('/CreateComment', methods = ["POST"])
@login_required
def create_comment():
    form = CommentForm()
    if form.validate_on_submit and current_user.is_authenticated:
        message = form.CommentContent.data
        user_ID = form.CreatorID.data
        poll_ID = form.PostID.data
        print("hello", poll_ID)
        comment = Comments(user_ID = user_ID, poll_ID = poll_ID, message = message)
        db.session.add(comment)
        db.session.commit()

        flash("Comment was successfully created.")
        return redirect(url_for('get_post', poll_id=int(poll_ID)))
    
    flash("Comment was too long. Please try again.")
    return redirect(url_for('get_post', poll_id=int(poll_ID)))

@app.route('/GetMostPopular/<choice>', methods=['GET'])
def popular_polls(choice):
    print(choice)
    if choice not in ["Daily", "Weekly", "Monthly"]:
        flash("Invalid option detected. Please try again.")
        return redirect(url_for("popular"))
    
    polls = get_timed_posts(choice)
    return render_template("PopularPolls.html", polls = polls)