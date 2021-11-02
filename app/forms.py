from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import InputRequired, Length, AnyOf, EqualTo, Regexp
from app.errorList import *

# Lab 4 -------------------------------------------------------------------------------------------------------------------------------------------------------------------
class LoginForm(FlaskForm):
    username = StringField('Логін', validators=[InputRequired('A username is required!'), Length(min=1, max=25, message="Логін повинен містити не менше 1 символа!")])
    password = PasswordField('Пароль', validators=[InputRequired('Password is required!'), AnyOf(values=['password', 'Serhiy'])])

# Lab 5 -------------------------------------------------------------------------------------------------------------------------------------------------------------------
class RegisterForm(FlaskForm):
    login = StringField('Логін *', validators=[InputRequired('Login is required')])
    password = PasswordField('Пароль *', validators=[InputRequired(error_0), Length(min=6, message=error_1)])
    password_r = PasswordField('Підтвердження паролю *', validators=[InputRequired(error_0), Length(min=6, message=error_1), EqualTo('password', message=error_2)])
    e_number = StringField('Номер *', validators=[InputRequired(error_3), Length(min=7, max=7, message=error_4), Regexp(regex='^[0-9]+$', message=error_5)])
    e_pin = PasswordField('Пін *', validators=[InputRequired(error_7), Length(min=4, max=4, message=error_6), Regexp(regex='^[0-9]+$', message=error_5)])
    e_year = SelectField('Рік *', choices=[2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021])
    d_series = StringField('Серія')
    d_number = StringField('Номер *')