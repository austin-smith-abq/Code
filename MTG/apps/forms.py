from flask_wtf import FlaskForm
from wtforms import StringField, SearchField, BooleanField, RadioField, DateField, SubmitField, SelectField
from wtforms.validators import DataRequired


class CardForm(FlaskForm):
    card_name = SearchField('Card Name', validators=[DataRequired()])
    submit = SubmitField('Submit')

class DeckForm(FlaskForm):
    deck_name = StringField('Deck Name', validators=[DataRequired()])
    submit = SubmitField('Submit')





