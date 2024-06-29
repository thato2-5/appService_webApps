from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length, Email

#Create a Search Form
class SearchForm(FlaskForm):
    search = StringField("Search...", validators = [DataRequired()])
    submit = SubmitField("submit")
    
#create Login Form
class LoginForm(FlaskForm):
    username = StringField("Username", validators = [DataRequired()])
    password = PasswordField("Password", validators = [DataRequired(), Length(min = 8)])
    submit = SubmitField("submit")

#Create Registration Form    
class RegistrationForm(FlaskForm):
    name = StringField("Name", validators = [DataRequired()])
    username = StringField("Username", validators = [DataRequired()])
    email = StringField("Email", validators = [DataRequired(), Email()])
    password1 = PasswordField("Password", validators = [DataRequired(), EqualTo('password2', message = "Passwords Must Match !"), Length(min = 8)])
    password2 = PasswordField("Confirm Password", validators = [DataRequired()])
    submit = SubmitField("submit")

# Create a Notes Form
class NoteForm(FlaskForm):
	title = StringField("Title", validators=[DataRequired()])
	description = TextAreaField("Description", validators=[DataRequired()])
	submit = SubmitField("Submit")
