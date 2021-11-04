from flask_wtf import FlaskForm
from .models import User
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo, Regexp, DataRequired, ValidationError
from app.errorList import *

# Lab 5 -------------------------------------------------------------------------------------------------------------------------------------------------------------------
class RegisterDoc(FlaskForm):
    email = StringField('Логін *', validators=[InputRequired('Login is required')])
    password = PasswordField('Пароль *', validators=[InputRequired(error_0), Length(min=6, message=error_1)])
    password_r = PasswordField('Підтвердження паролю *', validators=[InputRequired(error_0), Length(min=6, message=error_1), EqualTo('password', message=error_2)])
    e_number = StringField('Номер *', validators=[InputRequired(error_3), Length(min=7, max=7, message=error_4), Regexp(regex='^[0-9]+$', message=error_5)])
    e_pin = StringField('Пін *', validators=[InputRequired(error_7), Length(min=4, max=4, message=error_6), Regexp(regex='^[0-9]+$', message=error_5)])
    e_year = SelectField('Рік *', choices=[2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021])
    d_series = StringField('Серія')
    d_number = StringField('Номер *')

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
            raise ValidationError(error_15)

class LoginForm(FlaskForm):
    email = StringField('Логін', validators=[DataRequired(), Regexp('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField(label=(''))