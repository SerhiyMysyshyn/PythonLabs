from flask import Flask, render_template, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import InputRequired, Length, AnyOf, EqualTo, Regexp
from datetime import datetime
import os
import sys
import platform

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SerhiyMysyshyn'

# Lab 4 -------------------------------------------------------------------------------------------------------------------------------------------------------------------
class LoginForm(FlaskForm):
    username = StringField('Логін', validators=[InputRequired('A username is required!'), Length(min=1, max=25, message="Логін повинен містити не менше 1 символа!")])
    password = PasswordField('Пароль', validators=[InputRequired('Password is required!'), AnyOf(values=['password', 'Serhiy'])])

# Lab 5 -------------------------------------------------------------------------------------------------------------------------------------------------------------------
class RegisterForm(FlaskForm):
    login = StringField('Логін *', validators=[InputRequired('Login is required')])
    #   Error-list
    error_0 = 'Введіть пароль!'
    error_1 = 'Мінімальна довжина паролю 6 символів!'
    error_2 = 'Паролі повинні збігатися!'
    error_3 = 'Номер обов’язковий!'
    error_4 = 'Довжина числа повинна дорівнювати 7!'
    error_5 = 'Повинні бути лише цифри!'
    error_6 = 'Довжина PIN-коду має дорівнювати 4!'
    error_7 = 'Необхідний PIN-код!'
    error_8 = 'Не відповідає шаблону: XX (до 2015), або X00 (після 2015)!'
    error_9 = 'Не відповідає шаблону: (8 символів до 2015), або (6 символів після 2015)!'

    password = PasswordField('Пароль *', validators=[InputRequired(error_0), Length(min=6, message=error_1)])
    password_r = PasswordField('Підтвердження паролю *', validators=[InputRequired(error_0), Length(min=6, message=error_1), EqualTo('password', message=error_2)])
    e_number = StringField('Номер *', validators=[InputRequired(error_3), Length(min=7, max=7, message=error_4), Regexp(regex='^[0-9]+$', message=error_5)])
    e_pin = PasswordField('Пін *', validators=[InputRequired(error_7), Length(min=4, max=4, message=error_6), Regexp(regex='^[0-9]+$', message=error_5)])
    e_year = SelectField('Рік *', choices=[2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021])
    d_series = StringField('Серія')
    d_number = StringField('Номер *')

def getFooterData():
    OS_info = os.name + " " + platform.system() + " " + platform.release()
    current_datetime = datetime.now()
    userAgent = request.headers.get('User-Agent')
    pythonVersion = sys.version
    return [OS_info, pythonVersion, userAgent, current_datetime]

skills = ["Java Core and Pro", "MySQL", "SQL", "Kotlin", "Dagger 2", "OOP", "MVP", "MVVM", "REST-API", "Unit Testing",
          "RXJava", "Retrofit", "Git", "AndroidX", "Room Database", "UI layout / UI style xml", "Android SDK", "Google Maps / OSM API", "HTML / CSS / JS"]

projectsData = [
    {
        'name': 'Password Reminder',
        'imageURL': '/static/images/prog1.png',
        'android': 'Android 5.0',
        'description': 'Програма створена для збереження Ваших паролів та нагадування їх випадку, якщо Ви забули один із них!'
    },
    {
        'name': 'Cocomo/Cocomo II Calculator',
        'imageURL': '/static/images/prog2.png',
        'android': 'Android 5.0',
        'description': 'Програма створена для обчисленя трудоємності створення програм за допомогою калькуляторів Cocomo, Cocomo2 та Functional Points!'
    },
    {
        'name': 'Simple Weather',
        'imageURL': '/static/images/prog3.png',
        'android': 'Android 4.4',
        'description': 'Програма створена для відображення погоди в різних містах світу!'
    }
]

@app.route('/')
def home():
    return render_template('home.html', data=getFooterData())

@app.route('/about/')
def about():
    return render_template('about.html', data=getFooterData(), skills=skills)

@app.route('/myworks/')
def myworks():
    return render_template('myworks.html', data=getFooterData(), projectsData=projectsData)

# LAB 4 ---------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/form', methods=['POST', 'GET'])
def form():
    form = LoginForm()
    if form.validate_on_submit():
        if request.method == 'POST':
            if len(request.form['username']) > 5:
                flash('Форма надіслана успішно!', category='success')
                usernameData = form.username.data
                passwordData = form.password.data
                return render_template('form.html', form=form, usernameData=usernameData, passwordData=passwordData, data=getFooterData())
            else:
                #return '<h1>The username is {}. The password is {}.'.format(form.username.data, form.password.data)
                flash('Форма не відправлена! Рекомендація: постарайтесь придумати довший логін!', category='error')
                return render_template('form.html', form=form, data=getFooterData())

    return render_template('form.html', form=form, data=getFooterData())

# LAB 5 ---------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/registerForm', methods=['GET', 'POST'])
def registerForm():
    form = RegisterForm()
    if form.e_year.data is not None:
        regex = ''
        length = 0

        if int(form.e_year.data) < 2015:
            regex = '^[A-Z]{2}$'
            length = 8
        else:
            regex = '^[A-Z][0-9]{2}$'
            length = 6

        form.d_series.validators = [Regexp(regex=regex, message=form.error_8)]
        form.d_number.validators = [InputRequired(form.error_3), Length(min=length, max=length, message=form.error_9)]

    if form.validate_on_submit():
        from writeDataToFile import FileWriter
        FileWriter().write_to_file(form)
        return render_template("resultAfterRegister.html", form=form, data=getFooterData())

    return render_template("registerForm.html", form=form, data=getFooterData())

if __name__ == '__main__':
    app.run(debug=True)