from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField


class AssignForm(FlaskForm):
    TruckNumber = StringField('TruckNumber')
    LoadsDispatched = IntegerField('LoadsDispatched')
    submit = SubmitField('Assign')
