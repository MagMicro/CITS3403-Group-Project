from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/')
def index():
    print("User accessed the index page")
    return render_template('loginPage.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    print(f"User logged in with username: {username}, password: {password}")
    return render_template('loginPage.html')

@app.route('/create_account', methods=['POST'])
def create_account():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    print(f"User created an account with username: {username}, email: {email}, password: {password}")
    return render_template('loginPage.html')

@app.route('/create_account_page', methods=['GET'])
def create_account_page():
    print("User accessed the create account page")
    return render_template('accountCreationPage.html')

@app.route('/login_page', methods=['GET'])
def login_page():
    print("User accessed the login page")
    return render_template('loginPage.html')



if __name__ == '__main__':
    app.run(debug=True)
