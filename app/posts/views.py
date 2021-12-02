from ..auth.models import Posts
from flask import url_for, render_template, flash, request, redirect, abort, current_app
from .. import db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from .forms import CreatePostForm
from .getFunction import getFooterData, save_picture

from . import post_blueprint


@post_blueprint.route('/', methods=['GET', 'POST'])
def view_post():
    all_posts = Posts.query.all()
    image_file = url_for('static', filename='posts_pics/')
    return render_template('index.html', posts=all_posts, image_file=image_file, data=getFooterData())


@post_blueprint.route('/<pk>', methods=['GET', 'POST'])
def view_detail(pk):
    get_post = Posts.query.get_or_404(pk)
    return render_template('detail_post.html', pk=get_post, data=getFooterData())


@post_blueprint.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = CreatePostForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            image = picture_file
        else:
            image = 'postdefault.jpg'
        post = Posts(title=form.title.data, text=form.text.data, type=form.type.data, image_file=image, post_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('post.view_post'))
    return render_template('create_post.html', form=form, data=getFooterData())


@post_blueprint.route('/delete/<pk>', methods=['GET', 'POST'])
def delete_post(pk):
    get_post = Posts.query.get_or_404(pk)
    if current_user.id == get_post.post_id:
        db.session.delete(get_post)
        db.session.commit()
        return redirect(url_for('post.view_post'))
    flash('Ця дія заборонена! Пост не є ваш!', category='error')
    return redirect(url_for('post.view_detail', pk=pk))


@post_blueprint.route('/update/<pk>', methods=['GET', 'POST'])
def update_post(pk):
    get_post = Posts.query.get_or_404(pk)
    if current_user.id != get_post.post_id:
        flash('Ця дія заборонена! Пост не є ваш!', category='error')
        return redirect(url_for('post.view_detail', pk=pk))
    form = CreatePostForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            get_post.image_file = picture_file
        get_post.title = form.title.data
        get_post.text = form.text.data
        get_post.type = form.type.data
        db.session.commit()
        db.session.add(get_post)
        flash('Ви успішно редагували пост!', category='success')
        return redirect(url_for('post.view_detail', pk=pk))
    form.title.data = get_post.title
    form.text.data = get_post.text
    form.type.data = get_post.type
    return render_template('update_post.html', form=form, data=getFooterData())