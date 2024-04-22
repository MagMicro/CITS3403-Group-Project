from app import app
from flask import request, render_template, g, session, redirect, url_for
from app.forms import *
from .models import Users, Polls, VotePoll
from app import db

@app.route('/')
def index():
    username = session.get('username', 'Guest')
    return render_template('home.html', username=username)

@app.route('/home')
def home():
    return render_template('home.html')

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
            return render_template('home.html')

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
        return render_template(url_for('login'))
    else:
        return render_template('account.html')

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return render_template('home.html')

@app.route('/popular', methods=['GET'])
def popular():
    return render_template('popular.html')

@app.route('/ranking', methods=['GET'])
def ranking():
    return render_template('ranking.html')