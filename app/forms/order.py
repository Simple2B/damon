import enum

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.fields.core import SelectField


class StatusLevel(enum.Enum):
    InTransit = "InTransit"
    Delivered = "Delivered"
    Cancelled = "Cancelled"


class OrderForm(FlaskForm):

    CustomerName = StringField('CustomerName')
    JobName = StringField('JobName')
    destination = StringField('Destination')
    po = StringField('PO')
    city = SelectField('City', choices=[
        ('fw', 'Fort Worth'),
        ('dal', 'Dallas')
    ])
    MapscoLocation = StringField('MapscoLocation')
    JobNumber = StringField('JobNumber')
    MaterialName = StringField('MaterialName')
    LoadTotal = IntegerField('LoadTotal')
    Source = StringField('Source')
    lookup = SubmitField('LookUp')
    submit = SubmitField('Submit')
    Status = SelectField('Status', choices=[
        ('InTransit', 'InTransit'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled')
        ])
