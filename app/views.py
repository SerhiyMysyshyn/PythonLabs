from . import app
from flask import render_template, url_for, flash, redirect, session, request
from .forms import LoginForm, RegisterForm
#from app.models import User, Post
from app.getAdditionalData import *
from app.getFunction import getFooterData
from wtforms.validators import InputRequired, Length, Regexp


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