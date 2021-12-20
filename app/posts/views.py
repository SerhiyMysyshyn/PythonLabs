from .models import Post, Tag, Category
from .forms import PostForm, CategoryForm
from flask import url_for, render_template, flash, request, redirect, abort, current_app
from .. import db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from .getFunction import getFooterData, save_picture
from . import post_blueprint


@post_blueprint.route('/', methods=['GET', 'POST'])
def index():
    posts = Post.query.order_by(Post.created.desc())
    image = url_for('static', filename='posts_pics/')
    return render_template('index.html', posts=posts, image=image, data=getFooterData())


@post_blueprint.route('/<pk>', methods=['GET', 'POST'])
def view_detail(pk):
    get_post = Post.query.get_or_404(pk)
    return render_template('detail_post.html', pk=get_post, data=getFooterData())


@post_blueprint.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = PostForm()
    categories = Category.query.all()
    tags = Tag.query.all()

    form.category.choices = [(category.id, category.name)
                             for category in categories]
    form.tags.choices = [(tag.id, tag.name) for tag in tags]

    if form.validate_on_submit():
        if form.image.data:
            picture_file = save_picture(form.image.data)
            image = picture_file
        else:
            image = 'postdefault.jpg'

        tags = [Tag.query.get(tag_id) for tag_id in form.tags.data]
        post = Post(title=form.title.data,
                    description=form.description.data,
                    image=image,
                    user_id=current_user.id,
                    category_id=form.category.data,
                    tags=tags)

        db.session.add(post)
        db.session.commit()
        return redirect(url_for('post.index'))
    return render_template('create_post.html', form=form, data=getFooterData())


@post_blueprint.route('/delete/<pk>', methods=['GET', 'POST'])
def delete_post(pk):
    get_post = Post.query.get_or_404(pk)
    if current_user.id == get_post.user_id:
        db.session.delete(get_post)
        db.session.commit()
        return redirect(url_for('post.index'))
    flash('Ця дія заборонена! Пост не є ваш!', category='error')
    return redirect(url_for('post.view_detail', pk=pk))


@post_blueprint.route('/update/<pk>', methods=['GET', 'POST'])
def update_post(pk):
    post = Post.query.get_or_404(pk)
    if current_user.id != post.user_id:
        flash('Ця дія заборонена! Пост не є ваш!', category='error')
        return redirect(url_for('post.view_detail', pk=pk))
    form = PostForm()
    categories = Category.query.all()
    tags = Tag.query.all()

    form.category.choices = [(category.id, category.name)
                             for category in categories]
    form.tags.choices = [(tag.id, tag.name) for tag in tags]
    if form.validate_on_submit():
        if form.image.data:
            image = save_picture(form.image.data)
            post.image = image

        post.title = form.title.data
        post.description = form.description.data
        post.category_id = form.category.data
        post.tags = [Tag.query.get(tag_id) for tag_id in form.tags.data]

        db.session.commit()
        #db.session.add(get_post)
        flash('Ви успішно редагували пост!', category='success')
        return redirect(url_for('post.view_detail', pk=pk))

    form.category.data = post.category_id
    form.category.default = post.category_id
    form.tags.data = [tag.id for tag in post.tags]
    form.process()
    form.title.data = post.title
    form.description.data = post.description

    return render_template('update_post.html', form=form, data=getFooterData())

@post_blueprint.route('/categories', methods=['GET', 'POST'])
def categories():
    form = CategoryForm()
    if form.name.data:
        category = Category(name=form.name.data)
        db.session.add(category)
        db.session.commit()
        form.name.data = ''
        flash('Категорія ' + category.name + ' додана!', category='success')
    categories = Category.query.all()
    return render_template('categories.html', categories=categories, form=form, data=getFooterData())

@post_blueprint.route('/update_category/<id>', methods=['GET', 'POST'])
def update_post_category(id):
    category = Category.query.get_or_404(id)
    form = CategoryForm()
    if form.validate_on_submit():
        category.name = form.name.data

        db.session.add(category)
        db.session.commit()
        flash('Категорія відредагована успішно!', category='success')
        return redirect(url_for('.categories'))

    form.name.data = category.name
    categories = Category.query.all()
    return render_template('categories.html', categories=categories, form=form, data=getFooterData())

@post_blueprint.route('/delete_category/<id>', methods=['GET'])
@login_required
def delete_post_category(id):
    category = Category.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()

    flash('Категорія видалена успішно', category='success')
    return redirect(url_for('.categories'))



def get_category_name(id):
    return Category.query.get(id).name

current_app.jinja_env.globals.update(get_category_name=get_category_name)