from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, SelectField, StringField


class EditForm(FlaskForm):

    CustomerName = StringField('CustomerName')
    JobName = StringField('JobName')
    destination = StringField('Destination')
    po = StringField('PO')
    city = SelectField('City', choices=[
        ('fw', 'Fort Worth'),
        ('dal', 'Dallas')
    ])
    MapscoLocation = StringField('MapscoLocation')
    Source = StringField('Source')
    JobNumber = StringField('JobNumber')
    MaterialName = StringField('MaterialName')
    LoadTotal = IntegerField('LoadTotal')
    LoadDispatchTotal = IntegerField('LoadDispatchTotal')
    Status = SelectField('Status', choices=[
        ('InTransit', 'InTransit'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled')
        ])
    submit = SubmitField('Save')
