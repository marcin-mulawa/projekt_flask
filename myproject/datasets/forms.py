from flask_wtf import FlaskForm
from wtforms import StringField, FileField, SubmitField

class AddForm(FlaskForm):
    sign = StringField('Znak rozdzielający kolumny danych w pliku: ', default=';')
    files = FileField('Plik:')
    submit = SubmitField('Wrzuć plik na serwer')
