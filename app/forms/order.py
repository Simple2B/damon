import enum

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField


class StatusLevel(enum.Enum):
    InTransit = "InTransit"
    Delivered = "Delivered"
    Cancelled = "Cancelled"


class OrderForm(FlaskForm):

    CustomerName = StringField('CustomerName')
    JobName = StringField('JobName')
    MapscoLocation = StringField('MapscoLocation')
    JobNumber = StringField('JobNumber')
    MaterialName = StringField('MaterialName')
    LoadTotal = IntegerField('LoadTotal')
    Source = StringField('Source')
    lookup = SubmitField('LookUp')
    submit = SubmitField('Submit')
