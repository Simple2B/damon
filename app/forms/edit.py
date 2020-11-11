from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, SelectField, StringField


class EditForm(FlaskForm):

    CustomerName = StringField('CustomerName')
    JobName = StringField('JobName')
    MapscoLocation = StringField('MapscoLocation')
    Source = StringField('Source')
    JobNumberString = StringField('JobNumber')
    JobNumberSelect = SelectField('JobNumber')
    MaterialName = StringField('MaterialName')
    LoadTotal = IntegerField('LoadTotal')
    Status = SelectField('Status', choices=[
        ('InTransit', 'InTransit'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled')
        ])
    submit = SubmitField('Save')
