from app import app, db
from flask import request, render_template, g, session, redirect, url_for, jsonify, abort
from datetime import date, datetime
from app.forms import *
from .models import Users, Polls, VotePoll
import random

@app.route('/')
def index():
    return redirect(url_for('home'))

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

        user = Users.query.filter_by(username=username, password=password).first()
        if user is None:
            print("Login failed")
            return render_template('loginPage.html', form=form, message="Invalid username or password")
        else:
            print("Login successful")
            session['user_ID'] = user.user_ID
            session['username'] = user.username
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
            print("Username already taken")
            return render_template('accountCreationPage.html', form=form, title="Account Creation", message="Username already taken")

        user = Users.query.filter_by(email=email).first()
        if user is not None:
            print("Email already taken")
            return render_template('accountCreationPage.html', form=form, title="Account Creation", message="Email already taken")

        creation_date = date.today().strftime("%d/%m/%Y")
        new_user = Users(username=username, email=email, password=password, date=creation_date)
        db.session.add(new_user)
        db.session.commit()
        print("Account created")
        return render_template('loginPage.html', form=LoginForm(), title="Login", message="Account created successfully")

    print("User accessed the Account Creation page")
    return render_template('accountCreationPage.html', form=form, title="Account Creation")

@app.route('/account', methods=['POST', 'GET'])
def account():
    if 'username' not in session:
        return redirect(url_for('login'))
    else:
        user = Users.query.filter_by(user_ID=session["user_ID"]).first()
        return render_template('account.html', title="account", user=user)

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html', title="About")

@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/popular', methods=['GET'])
def popular():
    return render_template('popular.html', title="Popular")

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
            
        return render_template('ranking.html', title="Ranking", user=user, rank_data=rank_data)

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

        print(f"{creation_date}: User attempting to create a poll with options: {prompt}, {option1}, {option2} and tags: {tags}")

        new_poll = Polls(Option1=option1, Option2=option2, pollAuthor_ID=userID, tag1=tags[0], tag2=tags[1], tag3=tags[2], date=creation_date, prompt=prompt)
        db.session.add(new_poll)
        db.session.commit()
        print("Poll created")
        
        return redirect(url_for('home'))
    print("User accessed the create page")
    return render_template('create.html', form=form, title="Create", tags=tags)

@app.route('/GetUserPosts/<order>/<option>', methods=["GET"])
def generate_posts(order, option):
    posts = []
    for post in Users.query.filter_by(user_ID=session["user_ID"]).first().posts():
        posts.append(post.to_dict())
    if option == "Ascending":
        if order == "Popularity":
            posts.sort(key=lambda user_post: user_post["total"])
        elif order == "Difference":
            posts.sort(key=lambda user_post: abs(user_post["left%"] - user_post["right%"]))
        elif order == "UploadDate":
            posts.sort(key=lambda user_post: datetime.timestamp(datetime.strptime(user_post["date"], "%d/%m/%Y %H:%M:%S")))
    else:
        if order == "Popularity":
            posts.sort(reverse=True, key=lambda user_post: user_post["total"])
        elif order == "Difference":
            posts.sort(reverse=True, key=lambda user_post: abs(user_post["left%"] - user_post["right%"]))
        elif order == "UploadDate":
            posts.sort(reverse=True, key=lambda user_post: datetime.timestamp(datetime.strptime(user_post["date"], "%d/%m/%Y %H:%M:%S")))
    return render_template("UserPosts.html", posts=posts)

@app.route('/vote', methods=['GET'])
def display_vote_page():
    return render_template('vote.html')

@app.route('/api/poll/random', methods=['GET'])
def random_poll():
    if 'user_ID' not in session:
        return '', 401

    voted_polls = [vote.poll_ID for vote in VotePoll.query.filter_by(user_ID=session['user_ID']).all()]
    available_polls = Polls.query.filter(Polls.poll_ID.notin_(voted_polls)).all()

    if not available_polls:
        return jsonify({"message": "No available polls"}), 404

    random_poll = random.choice(available_polls)
    return jsonify(random_poll.to_dict())

@app.route('/api/poll/vote', methods=['POST'])
def cast_vote():
    if 'user_ID' not in session:
        return '', 401

    data = request.get_json()
    poll_id = data.get('poll_id')
    option = data.get('option')

    if not poll_id or option not in ['1', '2']:
        abort(400)

    user_vote = VotePoll.query.filter_by(user_ID=session['user_ID'], poll_ID=poll_id).first()
    if user_vote is not None:
        return '', 403

    new_vote = VotePoll(user_ID=session['user_ID'], poll_ID=poll_id, Vote_opt=int(option))
    db.session.add(new_vote)
    db.session.commit()

    poll = Polls.query.filter_by(poll_ID=poll_id).first()
    if not poll:
        abort(404)

    return jsonify(poll.to_dict())
