from flask_wtf import FlaskForm
from wtforms import StringField, SearchField, BooleanField, RadioField, DateField, SubmitField, SelectField
from wtforms.validators import DataRequired


class CardForm(FlaskForm):
    card_name = SearchField('Card name')
    submit = SubmitField('Submit')

