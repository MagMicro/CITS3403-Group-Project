from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField, BooleanField, SelectField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField("Username:", validators = [DataRequired()])
    password = PasswordField("Password:", validators = [DataRequired()])
    remember = BooleanField("Stay signed in: ")
    submit = SubmitField("Submit")

class CreationForm(FlaskForm):
    username = StringField("Username:", validators = [DataRequired()])
    email = EmailField("Email:", validators = [DataRequired()])
    password = PasswordField("Password:", validators = [DataRequired()])
    submit = SubmitField("Submit")

class PollForm(FlaskForm):
    prompt = StringField("Prompt: ", validators = [DataRequired()])
    option1 = StringField("Option 1:", validators = [DataRequired()])
    option2 = StringField("Option 2:", validators = [DataRequired()])
    tags = StringField("Tags:")
    submit = SubmitField("Submit")

    
class AccountDeletion(FlaskForm):
    password = PasswordField("Password:", validators = [DataRequired()])
    submit = SubmitField("Submit")
    
class PollSearch(FlaskForm):
    tags = ["Food", "Drink", "Sports", "Fashion", "Makeup", "Subject", "Video Games", "Anime", "Board Games" , "Animals", "People", "Places", "City", "Country", "Film", "TV", "Novels", "Abilities", "Historical", "Superheroes"]
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

class AccountPostFilter(FlaskForm):
    SortOption = SelectField("Sort by:", choices = ["Popularity", "Difference", "Date"])
    SortOrder = SelectField("Order by:", choices = ["Ascending", "Descending"])
