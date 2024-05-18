from app import db, bcrypt
from flask import request, render_template, g, session, redirect, url_for, jsonify, abort, flash, Blueprint
from app.forms import *
from .models import Users, Polls, VotePoll, Comments
from datetime import date, datetime
from app.Controller import *
import random
from flask_login import current_user, login_user, logout_user, login_required

main = Blueprint('main', __name__)


from flask_login import current_user, login_user, logout_user, login_required

@main.route('/')
def home():
    return render_template('home.html', search=PollSearch(), title="Home")

@main.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # Check if username matches a user in the database
        user = Users.query.filter_by(username=username).first()
        if user is None:
            flash("Username does not exist. Please try again.", "error")
            return render_template('loginPage.html', search=PollSearch(), form=form)
        
        # Check to see if the correct password, corresponding to the username, is provided
        elif user.check_password(password) == False:
            flash("Incorrect password. Please try again.", "error")
            return render_template('loginPage.html', search=PollSearch(), form=form)
        
        # If a valid username and password is provided, user is logged in
        else:
            flash("Login Successful: Welcome " + user.username)
            login_user(user, remember = form.remember.data)
            return redirect(url_for('main.home'))
    
    # Check if user has bypassed validation.
    check_validation_bypass()
    
    return render_template('loginPage.html', search=PollSearch(), form=form, title="Login")

@main.route('/create_account', methods=['POST', 'GET'])
def create_account():
    form = CreationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        user = Users.query.filter_by(username=username).first()
        # Case that the username used in creation is already taken.
        if user is not None:
            flash("Username is already taken. Please use a different one", "error")
            return render_template('accountCreationPage.html', search=PollSearch(), form=form, title = "Account Creation")

        # Case that the email used in creation is already taken.
        user = Users.query.filter_by(email=email).first()
        if user is not None:
            flash("Email is already taken. Please use a different one", "error")
            return render_template('accountCreationPage.html', search=PollSearch(), form=form, title = "Account Creation")

        # If a valid, unique username and password is provided, create the user account
        register_account(username, email, password)

        flash("Account created successfully.")
        return render_template('loginPage.html', search=PollSearch(), form=LoginForm(), title = "Login")
    
    # Check if user has bypassed validation.
    check_validation_bypass()
    return render_template('accountCreationPage.html', search=PollSearch(), form=form, title="Account Creation")

@main.route('/account', methods=['POST', 'GET'])
def account():
    # If the user is not logged in, redirect them to login page
    if current_user.is_anonymous:
        return redirect(url_for('main.login'))
    else:
        user = Users.query.get(current_user.user_ID)
        # Render html for deletion notification and pass to account page.
        notification = render_template("Notification.html", item = "post")
        return render_template('account.html', search=PollSearch(), title = "account",  user=user, deletion=AccountDeletion(), filter=AccountPostFilter(), form=AccountUsername(), notification = notification)

@main.route('/about', methods=['GET'])
def about():
    return render_template('about.html', search=PollSearch(), title="About")

@main.route('/logout', methods=['GET'])
@login_required
def logout():
    # If the requesting user is logged in, log their account out.
    logout_user()
    return redirect(url_for('main.home'))

@main.route('/popular', methods=['GET'])
def popular():
    return render_template('popular.html', search=PollSearch(), title="Popular")

@main.route('/ranking', methods=['GET'])
def ranking():
    # If the current user is not logged in, redirect them to login page.
    if current_user.is_anonymous:
        flash("You must be logged in to access the leaderboard.")
        return redirect(url_for('main.login'))
    else:
        user = Users.query.get(current_user.user_ID)
        ranked = Users.get_ranks()
        rank_data = []

        # Get the top 10 ranked users.
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

@main.route('/create', methods=['POST', 'GET'])
def create():
    # If the current user is not logged in, redirect them to login page.
    if current_user.is_anonymous:
        flash("You must be logged in to create posts.")
        return redirect(url_for('main.login'))
    
    tags = PollSearch().tags
    form = PollForm()
    PollBar = render_template('PollBar.html')

    if form.validate_on_submit():
        userID = current_user.user_ID
        # All post data normalised to prevent duplicate, capitalisation cases.
        prompt = form.prompt.data.capitalize()
        option1 = form.option1.data.capitalize()
        option2 = form.option2.data.capitalize()
        
        form_tags = form.tags.data.split(',')

        #Tags: Make sure all submitted tags are valid, and that there is atleast one
        #Post: Make sure options are different from eachother, and that the overall poll is unique
        if not (has_tags(form_tags) and valid_tags(tags, form_tags) and dif_options(option1, option2) and unique_post(option1, option2)):
            return render_template('create.html', search=PollSearch(), form=form, title = "Create", tags=tags, PollBar=PollBar)
        
        #Create new poll object
        create_poll(option1, option2, userID, prompt, form_tags)
        flash("Poll has been created successfully.")
        return redirect(url_for('main.home'))
    
    # Check if user has bypassed validation.
    check_validation_bypass()
    return render_template('create.html', search=PollSearch(), form=form, title="Create", tags=tags, PollBar=PollBar)

@main.route('/GetUserPosts/<option>/<order>', methods=["GET"])
@login_required
def generate_posts(option, order):
    posts = current_user.posts
    # Make sure the provided sorting options are valid
    if valid_choice(order, AccountPostFilter().SortOrder.choices) and valid_choice(option, AccountPostFilter().SortOption.choices):
        sort_by_option(option, get_sort_order(order), posts)
    else:
        return redirect(url_for("main.account"))
        
    return render_template("UserPosts.html", deletion = DeletionForm(), search=PollSearch(), posts = posts, url = url_for("main.home"))

@main.route('/DeletePost', methods = ['POST'])
@login_required
def delete_user_post():
    form = DeletionForm()
    if form.validate_on_submit():
        id = form.item_ID.data
        deleted_post = Polls.query.get(id)

        # Checks if the post can / is allowed to be deleted
        if verify_poll_deletion(deleted_post):
            deleted_post.wipe_poll()
            flash("Post was successfully deleted.")

        return redirect(url_for("main.account"))
    flash("Something went wrong. Please try again.")
    return redirect(url_for("main.account"))

@main.route('/DeleteComment', methods = ['POST'])
@login_required
def delete_user_comment():
    form = DeletionForm()
    if form.validate_on_submit():
        id = form.item_ID.data
        poll_id = form.comment_post_ID.data
        deleted_comment = Comments.query.get(id)

        # Checks if the comment can / is allowed to be deleted
        if verify_comment_deletion(deleted_comment):
            db.session.delete(deleted_comment)
            db.session.commit()
            flash("Comment was successfully deleted.")

        return redirect(url_for('main.get_post', poll_id=int(poll_id)))

@main.route("/DeleteAccount", methods = ["POST"])
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
            return redirect(url_for("main.login"))
        
        #Incorrect password provided
        else:
            flash("Invalid password. Please try again", "error")
            return redirect(url_for("main.account"))
        
    flash("Something went wrong. Please try again", "error")
    return redirect(url_for("main.account"))

@main.route('/api/poll/random', methods=['GET'])
def random_poll():
    if current_user.is_anonymous:
        available_polls = Polls.query.all()
        random_poll = random.choice(available_polls)

    else:
        voted_polls = [vote.poll_ID for vote in VotePoll.query.filter_by(user_ID=current_user.user_ID).all()]
        available_polls = Polls.query.filter(Polls.poll_ID.notin_(voted_polls)).filter(Polls.pollAuthor_ID.notin_([current_user.user_ID])).all()

        if not available_polls:
            flash("No more random polls available. Please try again later.")
            return redirect(url_for("main.home"))

        random_poll = random.choice(available_polls)
        
    notification = render_template("Notification.html", item = "comment")
    PollBar = render_template('PollBar.html', bar = bar_init(random_poll))
    return render_template('RandomPoll.html', submission=PollSubmissionForm(), poll = random_poll, search=PollSearch(), PollBar = PollBar, comment=CommentForm(), notification = notification), 200

@main.route('/api/poll/vote', methods=['POST'])
def cast_vote():
    # redirect anonymous users to the login page
    if current_user.is_anonymous:
        flash("You need to log in to vote.")
        return url_for("main.login"), 404
    
    data = request.get_json()
    poll_id = data.get('poll_id')
    option = data.get('option')

    # Invalid options are sent to the server.
    if not poll_id or option not in ['1', '2']:
        flash("Invalid voting option detected. Please try again.")
        return "", 400

    # Check if the user is allowed to vote
    if not vote_allowed(poll_id):
        return "", 403

    new_vote = VotePoll(user_ID=current_user.user_ID, poll_ID=poll_id, Vote_opt=int(option))
    db.session.add(new_vote)
    db.session.commit()
    return "", 200

@main.route('/Poll/<int:poll_id>', methods=['GET', 'POST'])
def get_post(poll_id):
    poll = Polls.query.get(poll_id)
    # Case that the user attempts to look for a pollID that currently doesnt exist
    if(poll is None):
        flash("Poll does not exist.")
        return redirect(url_for('main.home'))
    
    PollBar = render_template('PollBar.html', bar = bar_init(poll))
    notification = render_template("Notification.html", item = "comment")
    return render_template("IndividualPost.html",  deletion = DeletionForm(), search=PollSearch() , submission=PollSubmissionForm(), poll=poll, show_results=show_results(poll), PollBar = PollBar, comment=CommentForm(), notification = notification), 200
    
@main.route('/SearchOptions', methods=['POST'])
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
        return redirect(url_for("main.home"))

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
        return redirect(url_for("main.home"))

    # Validate the sort option (what to sort by)
    if valid_choice(option, PollSearch().SearchOption.choices):
        # Sort the list using the previously calculated order and the search option
        sort_by_option(option, mode, posts)
    else:
        # Invalid filter option was submitted
        flash("Invalid sort option detected. Please try again.", "error")
        return redirect(url_for("main.home"))

    return render_template("SearchResults.html", search=PollSearch(), posts=posts)

@main.route('/ChangeUsername', methods = ['POST'])
@login_required
def change_username():
    form = AccountUsername()
    if form.validate_on_submit():
        id = form.AccountID.data
        username = form.AccountUsername.data
        if current_user.is_authenticated and current_user.user_ID == id:
            if not valid_username(username) or not available_username(username):
                return redirect(url_for('main.account'))
            
            user = Users.query.get(id)
            user.username = username
            db.session.add(user)
            db.session.commit()
            flash("Username was successfully changed.")
            return redirect(url_for('main.account'))

    flash("You do not have permission to do this.")
    return redirect(url_for('main.account'))

@main.route('/CreateComment', methods = ["POST"])
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
        return redirect(url_for('main.get_post', poll_id=int(poll_ID)))
    
    flash("Comment was too long. Please try again.")
    return redirect(url_for('main.get_post', poll_id=int(poll_ID)))

@main.route('/GetMostPopular/<choice>', methods=['GET'])
def popular_polls(choice):
    print(choice)
    if choice not in ["Daily", "Weekly", "Monthly"]:
        flash("Invalid option detected. Please try again.")
        return redirect(url_for("main.popular"))
    
    polls = get_timed_posts(choice)
    return render_template("PopularPolls.html", polls = polls)