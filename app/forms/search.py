import enum

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class StatusLevel(enum.Enum):
        InTransit = "InTransit"
        Delivered = "Delivered"
        Cancelled = "Cancelled"

class SearchForm(FlaskForm):
#     assignID = StringField('assignID')
    CustomerName = StringField('CustomerName')
    JobName = StringField('JobName')
    MapscoLocation = StringField('MapscoLocation')
    JobNumber = IntegerField('JobNumber')
    MaterialName = StringField('MaterialName')
    LoadOutNum = IntegerField('LoadOutNum')
#     Loads = IntegerField('Loads')
    TruckNumber = IntegerField('TruckNumber')
    SubcontractorName = StringField('SubcontractorName')
#     Status = SelectField(choices=[('InTransit', 'InTransit'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled')])
    submit = SubmitField('Search')