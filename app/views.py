import json
from . import app, db
from flask import render_template, url_for, flash, redirect, session, abort
from .forms import RegisterDoc, RegisterForm, LoginForm
from .models import User
from app.getAdditionalData import *
from app.getFunction import getFooterData, write_to_json, validation
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/')
def home():
    return render_template('home.html', data=getFooterData())

@app.route('/about/')
def about():
    return render_template('about.html', data=getFooterData(), skills=skills)

@app.route('/myworks/')
def myworks():
    return render_template('myworks.html', data=getFooterData(), projectsData=projectsData)

# LAB 5 ---------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/registerForm', methods=['GET', 'POST'])
def formRegisterDoc():
    form = RegisterDoc()

    validation(form)

    if form.validate_on_submit():
        session['email'] = form.email.data
        if write_to_json(form):
            flash('Форма надіслана успішно! Дані успішно записані у json файл!', category='success')
        else:
            flash('Error', category='error')
        return redirect(url_for('formRegisterDoc'))

    try:
        sesiya = session['email']
        with open('MysyshynDB.json') as f:
            data_files = json.load(f)
        form.email.data = sesiya
        form.e_number.data = data_files[sesiya]['e_number']
        form.e_pin.data = data_files[sesiya]['e_pin']
        form.e_year.data = data_files[sesiya]['e_year']
        form.d_series.data = data_files[sesiya]['d_series']
        form.d_number.data = data_files[sesiya]['d_number']
    except:
        return render_template("registerForm.html", form=form, data=getFooterData())

    return render_template("registerForm.html", form=form, data=getFooterData())


# LAB 7 ---------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password1.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Ви успішно зареєстрували акаунт: { form.username.data } !', category='success')
        return redirect(url_for('login'))
    return render_template('register.html', form_reg=form, data=getFooterData())


@app.route("/logIn", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f'Ви ввійшли як користувач: {user.email}!', category='success')
            return redirect(url_for('account'))
        else:
            flash('Невірний пароль або логін!', category='error')
            return redirect(url_for('login'))

    return render_template('logIn.html', form=form, data=getFooterData())


@app.route("/users", methods=['GET', 'POST'])
@login_required
def users():
    all_users = User.query.all()
    count = User.query.count()
    if count == 0:
        abort(404)
    return render_template('userList.html', all_users=all_users, count=count, data=getFooterData())


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', data=getFooterData())

@app.route("/logout")
def logout():
    logout_user()
    flash('Ви успішно вийшли з облікового запису', category='success')
    return redirect(url_for('home'))

@app.route("/account")
@login_required
def account():
    return render_template('account.html', data=getFooterData())