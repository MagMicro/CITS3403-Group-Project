from app import app
from flask import request, render_template, g, session, redirect, url_for, jsonify, abort, flash
from app.forms import *
from .models import Users, Polls, VotePoll
from app import db
from datetime import date, datetime

from app.Controller import *
import random


from flask_login import current_user, login_user, logout_user, login_required

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title="Home")

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
            return render_template('loginPage.html', form=form)
        
        elif user.check_password(password) == False:
            flash("Invalid password. Please try again.", "error")
            return render_template('loginPage.html', form=form)
        
        else:
            flash("Login Successful: Welcome " + user.username)
            login_user(user, remember = form.remember.data)
            return redirect(url_for('home'))

    print("User accessed the login page")
    return render_template('loginPage.html', form=form, title="Login")

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
            return render_template('accountCreationPage.html', form=form, title = "Account Creation")

        user = Users.query.filter_by(email=email).first()
        if user is not None:
            flash("Email is already taken.", "error")
            return render_template('accountCreationPage.html', form=form, title = "Account Creation")

        creation_date = date.today().strftime("%d/%m/%Y")
        new_user = Users(username=username, email=email, date=creation_date)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        print("Account created")
        form = LoginForm()
        flash("Account created successfully.")
        return render_template('loginPage.html', form=form, title = "Login")

    print("User accessed the Account Creation page")
    return render_template('accountCreationPage.html', form=form, title="Account Creation")

@app.route('/account', methods=['POST', 'GET'])
def account():
    if current_user.is_anonymous:
        return redirect(url_for('login'))
    else:
        user = Users.query.filter_by(user_ID=current_user.user_ID).first()
        form = AccountDeletion()
        return render_template('account.html', title = "account",  user=user, form=form)

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html', title="About")

@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/popular', methods=['GET'])
def popular():
    return render_template('popular.html', title="Popular")

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
            
        return render_template('ranking.html', title="Ranking", user=user, rank_data=rank_data)

@app.route('/create', methods=['POST', 'GET'])
def create():
    if current_user.is_anonymous:
        return redirect(url_for('login'))
    
    tags = ["Food", "Drink", "Sports", "Fashion", "Makeup", "Subject", "Video Games", "Anime", "Board Games" , "Animals", "People", "Places", "City", "Country", "Film", "TV", "Novels", "Abilities", "Historical", "Superheroes"]
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
                return render_template('create.html', form=form, title = "Create", tags=tags, PollBar=PollBar)
        
        #Make sure all submitted tags are valid
        for tag in form_tags:
            if tag == "":
                flash("Need to use one or more tags. Please try again.", "error")
                return render_template('create.html', form=form, title = "Create", tags=tags, PollBar=PollBar)
            if tag not in tags:
                flash("Unrecognised tag/s detected. Please try again.", "error")
                return render_template('create.html', form=form, title = "Create", tags=tags, PollBar=PollBar)
        
        #Make sure the post is unique
        for post in Polls.query.filter_by(prompt=prompt):
            if (post.Option1 == option1 and post.Option2 == option2) or (post.Option1 == option2 and post.Option2 == option1):
                flash("Post already exists. Please try something else.", "error")
                return render_template('create.html', form=form, title = "Create", tags=tags, PollBar=PollBar)
        
        creation_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        print(f"{creation_date}: User attempting to create a poll with options:{prompt}, {option1}, {option2} and tags: {form_tags}")
        
        #Create new poll object
        new_poll = Polls(Option1=option1, Option2=option2, pollAuthor_ID=userID, date=creation_date, prompt=prompt)
        new_poll.add_tags(form_tags)

        db.session.add(new_poll)
        db.session.commit()
        print("Poll created")
        flash("Poll has been created successfully.")
        return redirect(url_for('home'))
    print("User accessed the create page")
    return render_template('create.html', form=form, title="Create", tags=tags, PollBar=PollBar)

@app.route('/GetUserPosts/<order>/<option>', methods=["GET"])
def generate_posts(order, option):
    posts = []
    for post in Users.query.filter_by(user_ID=current_user.user_ID).first().posts():
        posts.append(post.to_dict())

    if option == "Ascending":
        mode = False
    elif option == "Descending":
        mode = True
    else:
        flash("Invalid sort order detected. Please try again.", "error")
        return redirect(url_for("account"))

    if order == "Popularity":
        posts.sort(reverse=mode, key = lambda user_post: user_post["total"] )
    elif order == "Difference":
        posts.sort(reverse=mode, key = lambda user_post: abs(user_post["left%"] - user_post["right%"]))
    elif order == "UploadDate":
        posts.sort(reverse=mode, key = lambda user_post: datetime.timestamp(datetime.strptime(user_post["date"], "%d/%m/%Y %H:%M:%S")))
    else:
        flash("Invalid sort option detected. Please try again.", "error")
        return redirect(url_for("account"))
        
    return render_template("UserPosts.html", posts = posts)

@app.route('/DeletePost/<int:id>', methods = ['GET'])
@login_required
def delete_user_post(id):
    if(current_user.is_authenticated):
        deleted_post = Polls.query.get(id)

        if deleted_post is None:
            flash("Could not delete post. Post does not exist.")
        
        elif deleted_post.pollAuthor_ID != current_user.get_id():
            flash("You are not authorized to delete someone elses post.")

        else:
            deleted_post.delete_votes()
            db.session.delete(deleted_post)
            db.session.commit()
            flash("Post was successfully deleted.")
        return url_for("account")

    return url_for("login")

@app.route("/DeleteAccount", methods = ["POST"])
@login_required
def delete_account():
    form = AccountDeletion()
    if(form.validate_on_submit()):
        password = form.password.data

        #Verify the user's provided password
        if(current_user.check_password(password)):
            #Delete all content associated with a user and their posts
            for post in current_user.posts():
                post.delete_votes()
                db.session.delete(post)
    
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
    return render_template('RandomPoll.html')

@app.route('/api/poll/random', methods=['GET'])
def random_poll():
    if current_user.is_anonymous:
        available_polls = Polls.query.all()
        random_poll = random.choice(available_polls)
        return render_template('poll.html', poll = random_poll.to_dict()), 200

    else:
        voted_polls = [vote.poll_ID for vote in VotePoll.query.filter_by(user_ID=current_user.user_ID).all()]
        available_polls = Polls.query.filter(Polls.poll_ID.notin_(voted_polls)).filter(Polls.pollAuthor_ID.notin_([current_user.user_ID])).all()

        if not available_polls:
            return render_template('NoPolls.html'), 404

        random_poll = random.choice(available_polls)
        return render_template('poll.html', poll = random_poll.to_dict()), 200

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

    poll = Polls.query.filter_by(poll_ID=poll_id).first()
    if not poll:
        abort(404)
    poll = poll.to_dict()
    PollBar = render_template('PollBar.html', bar = bar_init(poll))
    return render_template('PollResults.html', poll = poll, PollBar = PollBar), 200

@app.route('/Poll/<int:id>', methods=['GET', 'POST'])
def get_post(id):
    post = Polls.query.get(id)

    # If the user is logged in, checks to see if they have already voted
    if current_user.is_authenticated:
        vote = VotePoll.query.filter_by(user_ID = current_user.user_ID, poll_ID = post.poll_ID)
    # Default no vote value of None, determines if poll results are shown when page is loaded
    else:
        vote = None

    # Case that the user attempts to look for a pollID that currently doesnt exist
    if(post is None):
        flash("Poll does not exist.")
        return redirect(url_for('home')), 404

    else:
        poll = post.to_dict()
        PollBar = render_template('PollBar.html', bar = bar_init(poll))
        return render_template("IndividualPost.html", poll=poll, vote=vote, PollBar = PollBar), 200