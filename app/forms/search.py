import enum

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField


class StatusLevel(enum.Enum):
    InTransit = "InTransit"
    Delivered = "Delivered"
    Cancelled = "Cancelled"


class SearchForm(FlaskForm):
    CustomerName = StringField('CustomerName')
    JobName = StringField('JobName')
    MapscoLocation = StringField('MapscoLocation')
    JobNumber = StringField('JobNumber')
    MaterialName = StringField('MaterialName')
    LoadOutNum = IntegerField('LoadOutNum')
    TruckNumber = IntegerField('TruckNumber')
    SubcontractorName = StringField('SubcontractorName')
    submit = SubmitField('Search')
