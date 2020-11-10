from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, SelectField, StringField


class EditForm(FlaskForm):


    CustomerName = StringField('CustomerName')
    JobName = StringField('JobName')
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
    submit = SubmitField('Edit')
