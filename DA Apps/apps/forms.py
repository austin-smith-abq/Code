from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SearchField, URLField, BooleanField, RadioField, DateField, SubmitField, SelectField
from wtforms.validators import DataRequired

class DocumentForm(FlaskForm):
    disable_auto_format = BooleanField('Disable auto-formatting')
    document_group = SelectField('Document group', choices=[1,2,3])
    document_type = SelectField('Document type', choices=[1,2,3])
    case_number = StringField('Case number', validators=[DataRequired()])
    submit = SubmitField('Submit')

#Might not use this
class PleaForm(FlaskForm):
    cms_case_num = StringField('DA number', validators=[DataRequired()])
    dist_docket_num = StringField('District court number', validators=[DataRequired()])
    defendant_name = StringField('Defendant name', validators=[DataRequired()])
    screener_name = StringField('Attorney who screened the charges', validators=[DataRequired()])
    screener_name = StringField('Attorney who screened the charges', validators=[DataRequired()])
    filed_dist_date = DateField('District court filed date', validators=[DataRequired()])
    assigned_date = DateField('Date assigned to you', validators=[DataRequired()])
    trial_date = DateField('Trial date', validators=[DataRequired()])
    tier = SelectField('Tier', choices=[1,2,3], validators=[DataRequired()])
    prior_plea = RadioField('Has there been a prior plea offer in this case?', choices=[('Yes', 'Yes'), ('No', 'No')], validators=[DataRequired()])
    plea_more_strict = RadioField('Are the terms of this plea offer more strict than the previous plea offer?', choices=[('Yes', 'Yes'), ('No', 'No')])
    all_open_cases_resolved = RadioField("Does your plea resolve all of the defendant's open cases?", choices=[('Yes', 'Yes'), ('No', 'No')])
    cases_not_resolved = StringField("What cases does it not resolve?")
    homicide = RadioField('Is this case a homicide?', choices=[('Yes', 'Yes'), ('No', 'No')])
    pdm_filed = RadioField('PDM filed?', choices=[('Yes', 'Yes'), ('No', 'No')])
    pdm_granted = RadioField('PDM granted?', choices=[('Yes', 'Yes'), ('No', 'No')])
    lea_victim = RadioField('Is the victim a law enforcement officer?', choices=[('Yes', 'Yes'), ('No', 'No')])
    submit = SubmitField('Submit')

class ContactSearchForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    search = SubmitField('Search')

class ContactForm(FlaskForm):
    agencies = ["Albuquerque Police Department", "Bernalillo County Sheriff's", "New Mexico State Police"]
    first_name = StringField('First name', validators=[DataRequired()])
    last_name = StringField('Last name', validators=[DataRequired()])
    agency = SelectField('Agency', choices=agencies, validators=[DataRequired()])
    badge_id = StringField('Badge ID', validators=[DataRequired()])
    title = StringField('Title')
    primary_phone = StringField('Primary phone')
    cell_phone = StringField('Cell phone')
    email = EmailField('Email')

    submit = SubmitField('Submit')

class UserSearchForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    search = SubmitField('Search')
    
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
    deactivate = SubmitField('Deactivate')

class GoogleSheetForm(FlaskForm):
    url = URLField('Sheet URL', validators=[DataRequired()])
    submit = SubmitField('submit')

