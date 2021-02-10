from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField


class FilterForm(FlaskForm):
    city = SelectField('City', choices=[
        ('', ''),
        ('fw', 'Fort Worth'),
        ('dal', 'Dallas')
    ])
    submit = SubmitField('Filter')
