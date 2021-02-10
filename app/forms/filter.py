from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.fields.core import DateField


class FilterForm(FlaskForm):
    city = SelectField('City', choices=[
        ('',''),
        ('fw', 'Fort Worth'),
        ('dal', 'Dallas')
    ])
    submit = SubmitField('Filter')
