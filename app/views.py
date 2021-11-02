import json
from . import app
from flask import render_template, url_for, flash, redirect, session, request
from .forms import LoginForm, RegisterForm
# from app.models import User, Post
from app.getAdditionalData import *
from app.getFunction import getFooterData, write_to_json, validation
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
                return render_template('form.html', form=form, usernameData=usernameData, passwordData=passwordData,
                                       data=getFooterData())
            else:
                flash('Форма не відправлена! Рекомендація: постарайтесь придумати довший логін!', category='error')
                return render_template('form.html', form=form, data=getFooterData())

    return render_template('form.html', form=form, data=getFooterData())


# LAB 5 ---------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/registerForm', methods=['GET', 'POST'])
def registerForm():
    form = RegisterForm()
    validation(form)

    if form.validate_on_submit():
        session['email'] = form.email.data
        if write_to_json(form):
            flash('Форма надіслана успішно! Дані успішно записані у json файл!', category='success')
        else:
            flash('Error', category='error')
        return redirect(url_for('registerForm'))

    try:
        sesiya = session['email']
    except:
        return render_template("registerForm.html", form=form, data=getFooterData())

    with open('MysyshynDB.json') as f:
        data_files = json.load(f)

    return render_template("registerForm.html",
                           form=form,
                           email=sesiya,
                           e_number=data_files[sesiya]['e_number'],
                           e_pin=data_files[sesiya]['e_pin'],
                           e_year=data_files[sesiya]['e_year'],
                           d_series=data_files[sesiya]['d_series'],
                           d_number=data_files[sesiya]['d_number'],
                           data=getFooterData())
