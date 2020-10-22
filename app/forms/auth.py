from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, Length, EqualTo

from app.models import User


class LoginForm(FlaskForm):
    UserID = StringField('user_id', [DataRequired()])
    Password = PasswordField('Password', [DataRequired()])
    submit = SubmitField('Login')