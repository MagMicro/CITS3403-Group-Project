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