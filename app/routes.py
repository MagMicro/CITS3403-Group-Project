from app import app
from flask import request, render_template, g, session, redirect, url_for, jsonify, abort
from app.forms import *
from .models import Users, Polls, VotePoll
from app import db
from datetime import date
from datetime import datetime

@app.route('/')
def index():
    return redirect(url_for('home'))

@app.route('/api/polls', methods=['GET'])
def get_polls():
    polls = Polls.query.all()
    user_votes = None
    polls_data = []

    for poll in polls:
        has_voted = False

        if VotePoll.query.filter_by(user_ID = session['user_ID'], poll_ID = poll.poll_ID).first() is not None:
            has_voted = True

        author = Users.query.filter_by(user_ID=poll.pollAuthor_ID).first()
        total_votes = VotePoll.query.filter_by(poll_ID=poll.poll_ID).count()
        votes1 = VotePoll.query.filter_by(poll_ID=poll.poll_ID, Vote_opt=1).count()
        votes2 = VotePoll.query.filter_by(poll_ID=poll.poll_ID, Vote_opt=2).count()

        poll_data = {
            'id': poll.poll_ID,
            'author': author.username if author else 'Unknown',
            'option1': poll.Option1,
            'votes1': (votes1 / total_votes) * 100 if total_votes > 0 else 0,
            'option2': poll.Option2,
            'votes2': (votes2 / total_votes) * 100 if total_votes > 0 else 0,
            'has_voted': has_voted
        }
        polls_data.append(poll_data)

    return jsonify(polls_data)

@app.route('/api/polls/<int:poll_id>/vote', methods=['POST'])
def vote(poll_id):
    # Check if user is logged in
    if 'user_ID' not in session:
        return '', 401

    # Get the selected option from the request body
    data = request.get_json()
    option = data.get('option')
    if option not in ['1', '2']:
        abort(400)

    # Record the vote
    vote = VotePoll(user_ID=session['user_ID'], poll_ID=poll_id, Vote_opt=int(option))
    #print vote for debug
    print(vote)

    #check if user has already voted
    user_vote = VotePoll.query.filter_by(user_ID=session['user_ID'], poll_ID=poll_id).first()
    if user_vote is not None:
        return '', 403
    
    db.session.add(vote)
    db.session.commit()

    return redirect(url_for('home'))

@app.route('/home')
def home():
    return render_template('home.html', title = "Home")


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        print(f"User attempted login with username: {username}, password: {password}")

        # Check if username and password match a user in the database
        user = Users.query.filter_by(username=username, password=password).first()
        if user is None:
            print("Login failed")
            return render_template('loginPage.html', form=form, message="Invalid username or password")
        else:
            print("Login successful")
            session['user_ID'] = user.user_ID
            session['username'] = user.username
            polls = Polls.query.all()
            return redirect(url_for('home'))

    print("User accessed the login page")
    return render_template('loginPage.html', form=form, title = "Login")

@app.route('/create_account', methods=['POST', 'GET'])
def create_account():
    form = CreationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        print(f"User attempting account creation with username: {username}, email: {email}, password: {password}")

        # Check if username is already taken
        user = Users.query.filter_by(username=username).first()
        if user is not None:
            print("Username already taken")
            return render_template('accountCreationPage.html', form=form, title = "Account Creation", message="Username already taken")

        # Check if email is already taken
        user = Users.query.filter_by(email=email).first()
        if user is not None:
            print("Email already taken")
            return render_template('accountCreationPage.html', form=form, title = "Account Creation", message="Email already taken")

        # Create account
        creation_date = date.today().strftime("%d/%m/%Y")
        new_user = Users(username=username, email=email, password=password, date=creation_date)
        db.session.add(new_user)
        db.session.commit()
        print("Account created")
        form = LoginForm()
        return render_template('loginPage.html', form=form, title = "Login", message="Account created successfully")

    print("User accessed the Account Creation page")
    return render_template('accountCreationPage.html', form=form, title="Account Creation")

@app.route('/account', methods=['POST', 'GET'])
def account():
    #print session details to console
    print(session)
    if 'username' not in session:
        return redirect(url_for('login'))
    else:
        user = Users.query.filter_by(user_ID=session["user_ID"]).first()
        return render_template('account.html', title = "account",  user=user)

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html', title = "About")

@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/popular', methods=['GET'])
def popular():
    return render_template('popular.html', title = "Popular")

@app.route('/ranking', methods=['GET'])
def ranking():
    if 'username' not in session:
        return redirect(url_for('login'))
    else:
        user = Users.query.filter_by(user_ID=session["user_ID"]).first()
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
            
        return render_template('ranking.html', title = "Ranking", user = user, rank_data = rank_data)

@app.route('/create', methods=['POST', 'GET'])
def create():
    if 'user_ID' not in session:
        return redirect(url_for('login'))
    
    tags = ["Food", "Sports", "Fashion", "Subject", "Video Games", "Anime", "Board Games" , "Animals", "People", "Places", "Film", "TV", "Novels", "Abilities", "Historical"]
    form = PollForm()

    if form.validate_on_submit():
        userID = session.get('user_ID')
        prompt = form.prompt.data
        option1 = form.option1.data
        option2 = form.option2.data 
        tags = form.tags.data.split(',')
        
        if len(tags) == 1 and tags[0] == '':
            tags = ["N/A", "N/A", "N/A"]
        else:
            tags += ['N/A'] * (3 - len(tags))

        creation_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        print(f"{creation_date}: User attempting to create a poll with options:{prompt}, {option1}, {option2} and tags: {tags}")
        

        new_poll = Polls(Option1=option1, Option2=option2, pollAuthor_ID=userID, tag1=tags[0], tag2=tags[1], tag3=tags[2], date=creation_date, prompt=prompt)
        db.session.add(new_poll)
        db.session.commit()
        print("Poll created")
        
        return redirect(url_for('home'))
    print("User accessed the create page")
    return render_template('create.html', form=form, title = "Create", tags=tags)
