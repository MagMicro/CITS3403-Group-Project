from app import app
from flask import request, render_template, g, session, redirect, url_for
from app.forms import *
import sqlite3

DATABASE = 'app/static/database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

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
    if(form.validate_on_submit()):
        username = form.username.data
        password = form.password.data
        print(f"User attempted login with username: {username}, password: {password}")
        db = get_db()
        cur = db.cursor()
        cur.execute('SELECT * FROM Users WHERE username = ? AND password = ?', (username, password))
        user = cur.fetchone()
        if user is None:
            print("Login failed")
            return render_template('loginPage.html', form = form, message="Invalid username or password")
        else:
            print("Login successful")
            session['user_ID'] = user[0]
            session['username'] = user[1]
            return render_template('home.html')
        
    print("User accessed the login page")
    return render_template('loginPage.html', form = form)

@app.route('/create_account', methods=['POST', 'GET'])
def create_account():
    form = CreationForm()
    if(form.validate_on_submit()):
        username = form.username.data
        email = form.email.data
        password = form.password.data
        print(f"User attempting account creation with username: {username}, email: {email}, password: {password}")
        db = get_db()
        cur = db.cursor()
        #check if username is already taken
        cur.execute('SELECT * FROM Users WHERE username = ?', (username,))
        user = cur.fetchone()
        if user is not None:
            print("Username already taken")
            return render_template('accountCreationPage.html', form = form, message="Username already taken")
    
        #check if email is already taken
        cur.execute('SELECT * FROM Users WHERE email = ?', (email,))
        user = cur.fetchone()
        if user is not None:
            print("Email already taken")
            return render_template('accountCreationPage.html', form = form, message="Email already taken")
    
        #create account
        cur.execute('INSERT INTO Users (username, email, password) VALUES (?, ?, ?)', (username, email, password))
        db.commit()
        print("Account created")
        form = LoginForm()
        return render_template('loginPage.html', form = form, message="Account created successfully")
    
    print("User accessed the Account Creation page")
    return render_template('accountCreationPage.html', form = form)

@app.route('/account', methods=['POST', 'GET'])
def account():
    #print session details to console
    print(session)
    if 'username' not in session:
        return render_template(url_for('login'))
    else:
        return render_template('account.html')