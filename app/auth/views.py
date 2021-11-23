from flask import render_template, url_for, flash, redirect, abort, current_app
from .forms import RegisterForm, LoginForm, UpdateAccountForm, ResetPasswordForm
from .. import db, bcrypt
from .models import User
from flask_login import login_user, current_user, logout_user, login_required
from .getFunction import getFooterData, save_picture
from datetime import datetime

from . import auth_blueprint

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
            flash('Invalid login!', category='error')
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
    return redirect(url_for('main_bp.home'))

@auth_blueprint.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Дані оновлено успішно!', category='success')
        return redirect(url_for('auth.account'))
    form.about_me.data = current_user.about_me
    form.username.data = current_user.username
    form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('auth/account.html', image_file=image_file, form=form, data=getFooterData())

@auth_blueprint.route("/reset-password", methods=['GET', 'POST'])
@login_required
def reset_password():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        current_user.password = bcrypt.generate_password_hash(form.new_password1.data).decode('utf-8')
        db.session.commit()
        flash('Пароль змінено успішно!', category='success')
        return redirect(url_for('auth.account'))
    return render_template('auth/reset_password.html', form=form, data=getFooterData())


@auth_blueprint.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_date = datetime.utcnow()
        db.session.commit()
