from flask import url_for, render_template, flash, request, redirect, abort, current_app
from .forms import AddSongsForm, CategoryForm
from . import songs_blueprint
from .models import categorysong, Songs
from .getFunctions import getFooterData
from .. import db
from flask_login import current_user, login_required

@songs_blueprint.route('/', methods=['GET', 'POST'])
@login_required
def view_songs():
    songs = Songs.query.order_by(Songs.songWriter).all()
    return render_template('view_songs.html', songs=songs, data=getFooterData())


@songs_blueprint.route('/addsongs', methods=['GET', 'POST'])
@login_required
def add_song():
    form = AddSongsForm()
    form.songCategory.choices = [(category.id, category.musicType) for category in categorysong.query.all()]
    if form.validate_on_submit():
        Song = Songs(songWriter=form.songWriter.data,
                     songName=form.songName.data,
                     songDescription=form.songDescription.data,
                     songDuration=form.songDuration.data,
                     songLink=form.songLink.data,
                     songCategory=form.songCategory.data,
                     songYear=form.songYear.data,
                     user_id=current_user.id)

        db.session.add(Song)
        db.session.commit()

        return redirect(url_for('songs.view_songs'))
    return render_template('songs_add.html', form=form, data=getFooterData())


@songs_blueprint.route('/<id>', methods=['GET', 'POST'])
def detail_song(id):
    songs = Songs.query.get_or_404(id)
    return render_template('songs_detail.html', pk=songs, data=getFooterData())


@songs_blueprint.route('/delete/<id>', methods=['GET', 'POST'])
def delete_song(id):
    songs = Songs.query.get_or_404(id)
    if current_user.id == songs.user_id:
        db.session.delete(songs)
        db.session.commit()
        return redirect(url_for('songs.view_songs'))

    flash('Це не ваш запис!', category='error')
    return redirect(url_for('songs.detail_songs', pk=id))


@songs_blueprint.route('/edit/<id>', methods=['GET', 'POST'])
def edit_song(id):
    songs = Songs.query.get_or_404(id)
    if current_user.id != songs.user_id:
        flash('Це не ваш запис!', category='error')
        return redirect(url_for('songs.detail_songs', pk=songs))

    form = AddSongsForm()
    form.songCategory.choices = [(category.id, category.musicType) for category in categorysong.query.all()]

    if form.validate_on_submit():
        songs.songWriter = form.songWriter.data
        songs.songName = form.songName.data
        songs.songDescription = form.songDescription.data
        songs.songDuration = form.songDuration.data
        songs.songLink = form.songLink.data
        songs.songCategory = form.songCategory.data
        songs.songYear = form.songYear.data

        db.session.add(songs)
        db.session.commit()

        flash('Пісня успішно змінена!', category='success')
        return redirect(url_for('songs.detail_song', id=id))

    form.songWriter.data = songs.songWriter
    form.songName.data = songs.songName
    form.songDescription.data = songs.songDescription
    form.songDuration.data = songs.songDuration
    form.songLink.data = songs.songLink
    form.songCategory.data = songs.songCategory
    form.songYear.data = songs.songYear

    return render_template('songs_add.html', form=form, data=getFooterData())


@songs_blueprint.route('/catacrcrud', methods=['GET', 'POST'])
def category_crud():
    form = CategoryForm()

    if form.validate_on_submit():
        category = categorysong(musicType=form.name.data)

        db.session.add(category)
        db.session.commit()
        flash('Категорія добавленна успішно!', category='success')
        return redirect(url_for('.category_crud'))

    categories = categorysong.query.all()
    return render_template('category_crud.html', categories=categories, form=form, data=getFooterData())


@songs_blueprint.route('/update_category/<id>', methods=['GET', 'POST'])
def update_category(id):
    category = categorysong.query.get_or_404(id)
    form = CategoryForm()
    if form.validate_on_submit():
        category.musicType = form.name.data

        db.session.add(category)
        db.session.commit()
        flash('Категорія відредагована успішно!', category='success')
        return redirect(url_for('.category_crud'))

    form.name.data = category.musicType
    categories = categorysong.query.all()
    return render_template('category_crud.html', categories=categories, form=form, data=getFooterData())


@songs_blueprint.route('/delete_category/<id>', methods=['GET'])
@login_required
def delete_category(id):
    category = categorysong.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()

    flash('Category delete', category='success')
    return redirect(url_for('.category_crud'))

