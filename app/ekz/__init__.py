from flask import Blueprint

ekz_blueprint = Blueprint('ekz', __name__)

from . import views