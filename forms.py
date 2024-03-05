from flask_wtf import FlaskForm
from wtforms import StringField, FileField, SubmitField
from wtforms.validators import DataRequired, Length

class UploadForm(FlaskForm):
    image = FileField("Carica l'imagine di quello che vuoi buttare", validators=[DataRequired()], id = "image")
    name = StringField("In quale comune d'Italia sei?", validators=[DataRequired(), Length(4, 40)], id = "comune_autocomplete")
    submit = SubmitField('Invia')

class ConfirmInputForm(FlaskForm):
    input_field = StringField('Cosa vuoi buttare?', validators=[Length(0, 40)], id = 'input_field')
    confirm_input = SubmitField('Conferma', id = 'confirm_input')