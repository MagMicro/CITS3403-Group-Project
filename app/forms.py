from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField, BooleanField, SelectField, IntegerField, TextAreaField, RadioField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField("Username:", validators = [DataRequired(), Length(min=5, max=15)])
    password = PasswordField("Password:", validators = [DataRequired()])
    remember = BooleanField("Stay signed in: ")
    submit = SubmitField("Submit")

class CreationForm(FlaskForm):
    username = StringField("Username:", validators = [DataRequired(), Length(min=5, max=15)])
    email = EmailField("Email:", validators = [DataRequired()])
    password = PasswordField("Password:", validators = [DataRequired()])
    submit = SubmitField("Submit")

class PollForm(FlaskForm):
    prompt = StringField("Prompt: ", validators = [DataRequired()])
    option1 = StringField("Option 1:", validators = [DataRequired()])
    option2 = StringField("Option 2:", validators = [DataRequired()])
    tags = StringField("Tags:")
    submit = SubmitField("Submit")

class PollSubmissionForm(FlaskForm):
    SubmissionOptions = RadioField(choices=[('1','option'),('2','option')])
    SubmissionSubmit = SubmitField("Vote")

class DeletionForm(FlaskForm):
    item_ID = IntegerField(validators = [DataRequired()])
    # Required by comments field
    comment_post_ID = IntegerField(validators = [DataRequired()])
    
class AccountDeletion(FlaskForm):
    password = PasswordField("Password:", validators = [DataRequired()])
    submit = SubmitField("Submit")
    
class PollSearch(FlaskForm):
    tags = ["Food", "Drink", "Sports", "Fashion", "Makeup", "Subject", "Video Games", "Anime", "Board Games" , "Card Games",
            "Animals", "Insects", "People", "Places", "City", "Country", "Film", "TV", "Novels", "Abilities", "Historical", 
            "Superheroes", "Villans", "Fiction", "Non-Fiction", "Sci-Fi", "Crime", "Horror", "Comedy" "Fantasy", "Cars",
            "Military", "Romance", "Franchise", "Corporation", "Transport", "Aviation", "Navel", "Colour", "Programming"]
    SearchBar = StringField()
    SearchPrompt = StringField("Prompt: ")
    SearchChoice1 = StringField("Option 1:")
    SearchChoice2 = StringField("Option 2:")

    Tag1 = SelectField("Search by:", choices = tags)
    Tag2 = SelectField("Search by:", choices = tags)
    Tag3 = SelectField("Search by:", choices = tags)

    SearchMode = SelectField("Search by:", choices = ["All", "PostID", "Username"])
    SearchOption = SelectField("Sort by:", choices = ["Popularity", "Difference", "Date"])
    SearchOrder = SelectField("Order by:", choices = ["Ascending", "Descending"])
    Voted = SelectField("Already voted:", choices = ["Both", "Yes", "No"])

class AccountPostFilter(FlaskForm):
    SortOption = SelectField("Sort by:", choices = ["Popularity", "Difference", "Date"])
    SortOrder = SelectField("Order by:", choices = ["Ascending", "Descending"])

class AccountUsername(FlaskForm):
    AccountUsername = StringField(validators = [DataRequired(), Length(min=5, max=15)])
    AccountID = IntegerField(validators = [DataRequired()])

class CommentForm(FlaskForm):
    CreatorID = IntegerField()
    PostID = IntegerField()
    CommentContent = TextAreaField(validators= [DataRequired(), Length(max=500)])
    CommentSubmit = SubmitField("Submit")