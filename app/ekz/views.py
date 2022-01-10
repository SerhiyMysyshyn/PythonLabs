from flask import Flask, g, request, jsonify
from functools import wraps

from .. import db

from . import ekz_blueprint
from ..songs.models import Songs

api_username = 'mysyshyn'
api_password = '2407'

def protected(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if auth and auth.username == api_username and auth.password == api_password:
            return f(*args, **kwargs)
        return jsonify({'message': 'Authentication failed!'}), 403
    return decorated

@ekz_blueprint.route('/songs', methods=['GET'])
@protected
def get_songs():
    songs = Songs.query.all()
    return_values = [{"id": song.id,
                      "writer": song.songWriter,
                      "name": song.songName,
                      "description": song.songDescription,
                      "duration": song.songDuration,
                      "link": song.songLink,
                      "category": song.category.musicType,
                      "year": song.songYear} for song in songs]

    return jsonify({'songs': return_values})

@ekz_blueprint.route('/songs/<int:id>', methods=['GET'])
@protected
def get_song(id):
    song = Songs.query.get_or_404(id)
    return jsonify({"id": song.id,
                      "writer": song.songWriter,
                      "name": song.songName,
                      "description": song.songDescription,
                      "duration": song.songDuration,
                      "link": song.songLink,
                      "category": song.category.musicType,
                      "year": song.songYear})


@ekz_blueprint.route('/songs', methods=['POST'])
def add_song():
    new_song_data = request.get_json()
    song = Songs.query.filter_by(songName=new_song_data['songName']).first()

    if song:
        return jsonify({"Message": "Song already exist"})

    sng = Songs(
        songWriter=new_song_data['songWriter'],
        songName=new_song_data['songName'],
        songDescription=new_song_data['songDescription'],
        songDuration=new_song_data['songDuration'],
        songLink=new_song_data['songLink'],
        songCategory=new_song_data['songCategory'],
        songYear=new_song_data['songYear'],
        user_id=new_song_data['user_id']
    )
    print(new_song_data['songName'])
    print(new_song_data['songName'])
    db.session.add(sng)
    db.session.commit()
    return jsonify({"id": sng.id,
                      "writer": sng.songWriter,
                      "name": sng.songName,
                      "description": sng.songDescription,
                      "duration": sng.songDuration,
                      "link": sng.songLink,
                      "category": sng.songCategory,
                      "year": sng.songYear})

@ekz_blueprint.route('/songs/<int:id>', methods=['PUT', 'PATCH'])
@protected
def edit_song(id):
    song = Songs.query.get(id)
    if not song:
        return jsonify({"Message": "Song does not exist"})

    update_song_data = request.get_json()
    songs = Songs.query.filter_by(songName=update_song_data['songName']).first()
    if songs:
        return jsonify({"Message": "Song already exist"})

    song.songWriter = update_song_data['songWriter']
    song.songName = update_song_data['songName']
    song.songDescription = update_song_data['songDescription']
    song.songDuration = update_song_data['songDuration']
    song.songLink = update_song_data['songLink']
    song.songCategory = update_song_data['songCategory']
    song.songYear = update_song_data['songYear']
    song.user_id = update_song_data['user_id']

    db.session.add(song)
    db.session.commit()

    return jsonify({"id": song.id,
                      "writer": song.songWriter,
                      "name": song.songName,
                      "description": song.songDescription,
                      "duration": song.songDuration,
                      "link": song.songLink,
                      "category": song.songCategory,
                      "year": song.songYear})


@ekz_blueprint.route('/songs/<int:id>', methods=['DELETE'])
@protected
def delete_song(id):
    song = Songs.query.get_or_404(id)
    db.session.delete(song)
    db.session.commit()

    return jsonify({'Message': 'The song has been deleted!'})
