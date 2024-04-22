from app import app
from flask import request, render_template, g, session, redirect, url_for
from app.forms import *
from .models import Users, Polls, VotePoll
from app import db

@app.route('/')
def index():
    return redirect(url_for('home'))

@app.route('/home')
def home():
    polls = Polls.query.all()
    user_votes = None
    polls_data = []

    if 'user_ID' in session:
        user_votes = VotePoll.query.filter_by(user_ID=session['user_ID']).all()

    for poll in polls:
        has_voted = False
        if user_votes and poll.poll_ID in [vote.poll_ID for vote in user_votes]:
            has_voted = True

        author = Users.query.filter_by(user_ID=poll.pollAuthor_ID).first()

        total_votes = VotePoll.query.filter_by(poll_ID=poll.poll_ID).count()
        votes1 = VotePoll.query.filter_by(poll_ID=poll.poll_ID, Vote_opt=1).count()
        votes2 = VotePoll.query.filter_by(poll_ID=poll.poll_ID, Vote_opt=2).count()

        poll_data = {
            'author': author.username if author else 'Unknown',
            'option1': poll.Option1,
            'votes1': (votes1 / total_votes) * 100 if total_votes > 0 else 0,
            'option2': poll.Option2,
            'votes2': (votes2 / total_votes) * 100 if total_votes > 0 else 0,
            'has_voted': has_voted
        }
        polls_data.append(poll_data)

    return render_template('home.html', polls=polls_data)


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
    return render_template('loginPage.html', form=form)

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
            return render_template('accountCreationPage.html', form=form, message="Username already taken")

        # Check if email is already taken
        user = Users.query.filter_by(email=email).first()
        if user is not None:
            print("Email already taken")
            return render_template('accountCreationPage.html', form=form, message="Email already taken")

        # Create account
        new_user = Users(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        print("Account created")
        form = LoginForm()
        return render_template('loginPage.html', form=form, message="Account created successfully")

    print("User accessed the Account Creation page")
    return render_template('accountCreationPage.html', form=form)

@app.route('/account', methods=['POST', 'GET'])
def account():
    #print session details to console
    print(session)
    if 'username' not in session:
        return redirect(url_for('login'))
    else:
        return render_template('account.html')

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/popular', methods=['GET'])
def popular():
    return render_template('popular.html')

@app.route('/ranking', methods=['GET'])
def ranking():
    return render_template('ranking.html')

@app.route('/create', methods=['POST', 'GET'])
def create():
    
    if 'user_ID' not in session:
        return redirect(url_for('login'))
    
    form = PollForm()
    if form.validate_on_submit():
        userID = session.get('user_ID')
        
        option1 = form.option1.data
        option2 = form.option2.data
        
        print(f"User attempting to create a poll with options: {option1}, {option2}")

        new_poll = Polls(Option1=option1, Option2=option2, pollAuthor_ID=userID)
        db.session.add(new_poll)
        db.session.commit()
        print("Poll created")
        
        return redirect(url_for('home'))
    print("User accessed the create page")
    return render_template('create.html', form=form)
