from app import app
from flask import Flask, request, render_template, g
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
    print("User accessed the index page")
    return render_template('loginPage.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    print(f"User attempted login with username: {username}, password: {password}")
    db = get_db()
    cur = db.cursor()
    cur.execute('SELECT * FROM Users WHERE username = ? AND password = ?', (username, password))
    user = cur.fetchone()
    if user is None:
        print("Login failed")
        return render_template('loginPage.html', message="Invalid username or password")
    else:
        print("Login successful")
        return render_template('home.html', user_ID=user[0], username=user[1])

@app.route('/create_account', methods=['POST'])
def create_account():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    print(f"User attempting account creation with username: {username}, email: {email}, password: {password}")
    db = get_db()
    cur = db.cursor()
    #check if username is already taken
    cur.execute('SELECT * FROM Users WHERE username = ?', (username,))
    user = cur.fetchone()
    if user is not None:
        print("Username already taken")
        return render_template('accountCreationPage.html', message="Username already taken")
    
    #check if email is already taken
    cur.execute('SELECT * FROM Users WHERE email = ?', (email,))
    user = cur.fetchone()
    if user is not None:
        print("Email already taken")
        return render_template('accountCreationPage.html', message="Email already taken")
    
    #create account
    cur.execute('INSERT INTO Users (username, email, password) VALUES (?, ?, ?)', (username, email, password))
    db.commit()
    print("Account created")
    return render_template('loginPage.html', message="Account created successfully")

@app.route('/create_account_page', methods=['GET'])
def create_account_page():
    print("User accessed the create account page")
    return render_template('accountCreationPage.html')

@app.route('/login_page', methods=['GET'])
def login_page():
    print("User accessed the login page")
    return render_template('loginPage.html')