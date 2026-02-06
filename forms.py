from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, DateField, IntegerField, FloatField, SelectField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Optional, NumberRange

class ProjectForm(FlaskForm):
    project_name = StringField('Fejlesztés neve', validators=[DataRequired()])
    description = TextAreaField('Leírás', validators=[Optional()])
    developer_name = StringField('Fejlesztő neve', validators=[DataRequired()])

    status = SelectField('Státusz', choices=[
        ('Új', 'Új'),
        ('Folyamatban', 'Folyamatban'),
        ('Tesztelés', 'Tesztelés'),
        ('Kész', 'Kész'),
        ('Élesítve', 'Élesítve'),
        ('Felfüggesztve', 'Felfüggesztve')
    ], validators=[DataRequired()])

    arrival_date = DateField('Beérkezés ideje', format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField('Fejlesztés vége', format='%Y-%m-%d', validators=[Optional()])

    percentage = IntegerField('Készültség (%)', validators=[
        NumberRange(min=0, max=100, message="0 és 100 közötti értéknek kell lennie.")
    ], default=0)

    fte = FloatField('FTE', validators=[Optional()])
    requestor = StringField('Igénylő', validators=[DataRequired()])

    # Files - No restrictions on file type
    doc_business = FileField('Üzleti igény', validators=[Optional()])
    doc_test = FileField('Tesztjegyzőkönyv', validators=[Optional()])
    doc_ops = FileField('Üzemeltetési dokumentáció', validators=[Optional()])

    submit = SubmitField('Mentés')
