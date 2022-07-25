from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired


class DocumentForm(FlaskForm):
    disable_auto_format = BooleanField('Disable auto-formatting')
    document_group = SelectField('Document group', choices=[1,2,3])
    document_type = SelectField('Document type', choices=[1,2,3])
    case_number = StringField('Enter a case number', validators=[DataRequired()])
    submit = SubmitField('Submit')

class UserSearchForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Search')
    
class UserForm(FlaskForm):
    user_types = ['Standard', 'Intern', 'Contractor']
    divisions = ['SAKI', 'General Crimes']
    titles = ['Legal Secretary', 'IT Administrator']
    first_name = StringField('First name', validators=[DataRequired()])
    last_name = StringField('Last name', validators=[DataRequired()])
    user_type = SelectField('User Type', choices=user_types, validators=[DataRequired()])
    user_id = StringField('User ID', validators=[DataRequired()])
    division = SelectField('Division', choices=divisions)
    title = SelectField('Title', choices=titles)
    supervisor = BooleanField('Is this user a supervisor?')
    submit = SubmitField('Submit')

