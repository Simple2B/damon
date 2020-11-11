from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField


class AssignForm(FlaskForm):
    TruckNumberString = StringField('TruckNumber')
    TruckNumberSelect = SelectField('TruckNumber')
    LoadsDispatched = IntegerField('LoadsDispatched')
    submit = SubmitField('Assign')
