from flask import render_template, url_for, flash, redirect, abort
from .forms import RegisterForm, LoginForm
from .. import db
from .models import User
from flask_login import login_user, current_user, logout_user, login_required
from . import auth_blueprint
from .getFunction import getFooterData

@auth_blueprint.route('/')
def index():
    return '[ ✔ ]'

# LAB 7 ---------------------------------------------------------------------------------------------------------------------------------------------------------
@auth_blueprint.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password1.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Ви успішно зареєстрували акаунт: { form.username.data } !', category='success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form_reg=form, data=getFooterData())


@auth_blueprint.route("/logIn", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f'Ви ввійшли як користувач: {user.email}!', category='success')
            return redirect(url_for('auth.account'))
        else:
            flash('Невірний пароль або логін!', category='error')
            return redirect(url_for('auth.login'))

    return render_template('auth/logIn.html', form=form, data=getFooterData())


@auth_blueprint.route("/users", methods=['GET', 'POST'])
@login_required
def users():
    all_users = User.query.all()
    count = User.query.count()
    if count == 0:
        abort(404)
    return render_template('auth/userList.html', all_users=all_users, count=count, data=getFooterData())


@auth_blueprint.route("/logout")
def logout():
    logout_user()
    flash('Ви успішно вийшли з облікового запису', category='success')
    return redirect(url_for('home'))

@auth_blueprint.route("/account")
@login_required
def account():
    return render_template('auth/account.html', data=getFooterData())