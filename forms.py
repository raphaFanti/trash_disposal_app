from flask_wtf import FlaskForm
from wtforms import StringField, FileField, SubmitField
from wtforms.validators import DataRequired, Length

class UploadForm(FlaskForm):
    image = FileField("Carica l'imagine di quello che vuoi buttare", validators=[DataRequired()], id = "image")
    dispose_location = StringField("In quale comune d'Italia sei?", validators=[DataRequired(), Length(4, 40)], id = "comune_autocomplete")
    submit = SubmitField('Invia')

class ConfirmInputForm(FlaskForm):
    input_field = StringField("Espliciti l'oggetto da buttare:", validators=[Length(0, 40)], id = 'input_field')
    confirm_input = SubmitField('Conferma oggetto proposto', id = 'confirm_input_button')
    confirm_edited_input = SubmitField('Conferma', id = 'confirm_edited_input_button')