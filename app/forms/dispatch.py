from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField


class DispatchForm(FlaskForm):
    TruckNumber = StringField('TruckNumber')
    LoadsDispatched = IntegerField('LoadsDispatched')
    submit = SubmitField('Add New Dispatch')
