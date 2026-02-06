from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, DateField, IntegerField, FloatField, SelectField, SubmitField
from wtforms.validators import DataRequired, Optional, NumberRange

class ProjectForm(FlaskForm):
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

    # Files
    doc_business = FileField('Üzleti igény (doc, docx, pdf)', validators=[
        Optional(),
        FileAllowed(['doc', 'docx', 'pdf'], 'Csak dokumentumok tölthetők fel!')
    ])
    doc_test = FileField('Tesztjegyzőkönyv (doc, docx, pdf, xlsx)', validators=[
        Optional(),
        FileAllowed(['doc', 'docx', 'pdf', 'xlsx', 'xls'], 'Csak dokumentumok tölthetők fel!')
    ])
    doc_ops = FileField('Üzemeltetési dokumentáció (doc, docx, pdf)', validators=[
        Optional(),
        FileAllowed(['doc', 'docx', 'pdf'], 'Csak dokumentumok tölthetők fel!')
    ])

    submit = SubmitField('Mentés')
