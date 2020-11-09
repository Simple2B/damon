from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    UserID = StringField('user_id', [DataRequired()])
    Password = PasswordField('Password', [DataRequired()])
    submit = SubmitField('Login')
