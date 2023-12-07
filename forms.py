from flask_wtf import FlaskForm
from wtforms import StringField, FileField, SubmitField
from wtforms.validators import DataRequired, Length

class UploadForm(FlaskForm):
    image = FileField("Carica l'imagine di quello che vuoi buttare", validators=[DataRequired()])
    name = StringField("In quale comune d'Italia sei?", validators=[DataRequired(), Length(10, 40)])
    submit = SubmitField('Invia')