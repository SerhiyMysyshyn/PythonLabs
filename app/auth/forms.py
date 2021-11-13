from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import InputRequired, Length, EqualTo, Regexp, DataRequired, ValidationError
from app.errorList import *
from .models import User

# Lab 7 -------------------------------------------------------------------------------------------------------------------------------------------------------------------
class RegisterForm(FlaskForm):
    username = StringField("Ім'я", validators=[InputRequired(error_10), Length(min=4, max=14, message=error_11), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, error_12)])
    email = StringField('E-mail', validators=[InputRequired(error_13), Regexp('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', message=error_14)])
    password1 = PasswordField('Пароль', validators=[InputRequired(error_0), Length(min=6, message=error_1)])
    password2 = PasswordField('Повторіть пароль', validators=[InputRequired(error_0),Length(min=6, message=error_1), EqualTo('password1', message=error_2)])
    submit = SubmitField(label=(''))

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(error_15)

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError(error_16)

class LoginForm(FlaskForm):
    email = StringField('Логін', validators=[DataRequired(), Regexp('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember = BooleanField('')
    submit = SubmitField(label=(''))