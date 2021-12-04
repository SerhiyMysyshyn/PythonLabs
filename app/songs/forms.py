from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField, IntegerField
from wtforms.validators import Length, DataRequired, InputRequired
from flask_wtf.file import FileField, FileAllowed

class AddSongsForm(FlaskForm):
    songWriter = StringField('Автори', validators=[InputRequired(), Length(min=5, max=100)])
    songName = StringField('Назва', validators=[InputRequired(), Length(min=5, max=120)])
    songDescription = TextAreaField('Опис', validators=[Length(max=2500)])
    songDuration = StringField('Тривалість', validators=[InputRequired(), Length(min=3, max=15)])
    songLink = StringField('Посилання на кліп', validators=[InputRequired(), Length(min=2, max=250)])
    songCategory = SelectField(u'Тип музики', coerce=int)
    songYear = IntegerField('Рік виходу', validators=[DataRequired()])
    submit = SubmitField('')

class CategoryForm(FlaskForm):
    name = StringField("Ім'я категорії", validators=[DataRequired(), Length(min=0, max=60)])
    submit = SubmitField('')