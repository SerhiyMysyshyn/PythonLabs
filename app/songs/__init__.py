from flask import Blueprint

songs_blueprint = Blueprint('songs', __name__, template_folder="templates/songs")

from . import views