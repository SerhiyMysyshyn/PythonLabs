from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import Length, DataRequired, InputRequired
from flask_wtf.file import FileField, FileAllowed


class CreatePostForm(FlaskForm):
    title = StringField('Заголовок', validators=[InputRequired(), Length(min=2, max=60)])
    text = TextAreaField('Вміст', validators=[Length(max=500)])
    picture = FileField('Завантажте фото для публікації', validators=[FileAllowed(['jpg', 'png'])])
    type = SelectField('Тип', choices=[('News', 'News'), ('Publication', 'Publication'), ('Other', 'Other')])
    submit = SubmitField('')