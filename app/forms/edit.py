from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, SelectField


class EditForm(FlaskForm):
    loads = IntegerField('Loads')
    status = SelectField('Status', choices=[('InTransit', 'InTransit'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled')])
    submit = SubmitField('Edit')
