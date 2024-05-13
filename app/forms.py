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
    SearchBar = StringField()
    SearchPrompt = StringField("Prompt: ")
    SearchChoice1 = StringField("Option 1:")
    SearchChoice2 = StringField("Option 2:")
    SearchMode = SelectField("Search by:", choices = ["All", "User ID", "Post ID"])
    SearchOption = SelectField("Sort by:", choices = ["Popularity", "Difference", "Upload Date"])
    SearchOrder = SelectField("Order by:", choices = ["Ascending", "Descending"])
