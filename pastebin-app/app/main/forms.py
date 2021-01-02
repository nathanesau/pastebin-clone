from flask import request
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length
from wtforms import TextAreaField, SubmitField, StringField, RadioField, Field


class PasteForm(FlaskForm):
    # static variables
    paste_tags = []

    form_type = 'Paste'
    paste = TextAreaField('Say something', validators=[DataRequired()])
    tag = StringField('Tags')  # autocomplete
    tagbtn = SubmitField('add tag')    
    expires = RadioField('Expires', choices=[('Never', 'Never'),
        ('1 Hour', '1 Hour'),
        ('1 Day', '1 Day'),
        ('1 Week', '1 Week')])
    submit = SubmitField('Submit')
