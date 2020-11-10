import enum

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField


class StatusLevel(enum.Enum):
    InTransit = "InTransit"
    Delivered = "Delivered"
    Cancelled = "Cancelled"


class OrderForm(FlaskForm):
    choices = []

    CustomerName = StringField('CustomerName')
    JobName = StringField('JobName')
    MapscoLocation = StringField('MapscoLocation')
    JobNumber = SelectField('JobNumber', coerce=int)
    MaterialName = StringField('MaterialName')
    LoadTotal = IntegerField('LoadTotal')
    Source = StringField('Source')
    submit = SubmitField('Submit')
