from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField

class AddForm(FlaskForm):

    files = FileField('file')
    submit = SubmitField('Add File')
