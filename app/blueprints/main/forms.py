from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
            
class SearchForm(FlaskForm):
    class Meta:
        csrf = False
    search = StringField('Search', validators=[DataRequired()])
    submit = SubmitField('Submit')
    