from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField, BooleanField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField("Username:", validators = [DataRequired()])
    password = PasswordField("Password:", validators = [DataRequired()])
    submit = SubmitField("Submit")

class CreationForm(FlaskForm):
    username = StringField("Username:", validators = [DataRequired()])
    email = EmailField("Email:", validators = [DataRequired()])
    password = PasswordField("Password:", validators = [DataRequired()])
    TOS = BooleanField("TOS:")
    submit = SubmitField("Submit")

class PollForm(FlaskForm):
    option1 = StringField("Option 1:", validators = [DataRequired()])
    option2 = StringField("Option 2:", validators = [DataRequired()])
    sumbit = SubmitField("Submit")