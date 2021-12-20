from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField, SelectMultipleField
from wtforms.validators import Length, DataRequired, InputRequired
from flask_wtf.file import FileField, FileAllowed


class PostForm(FlaskForm):
    title = StringField('Заголовок', validators=[InputRequired(), Length(min=2, max=60)])
    description = TextAreaField('Опис', validators=[Length(max=500)])
    image = FileField('Завантажити фото', validators=[FileAllowed(['jpg', 'png'])])
    category = SelectField('Категорія', validators=[InputRequired()])
    tags = SelectMultipleField("Теги", validators=[InputRequired()], coerce=int)
    submit = SubmitField('')

class CategoryForm(FlaskForm):
    name = StringField('Назва', validators=[InputRequired(), Length(min=2, max=50)])
    submit = SubmitField('')