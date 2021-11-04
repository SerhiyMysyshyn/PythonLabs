import os
basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = 'SerhiyMysyshyn'
WTF_CSRF_ENABLED = True

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'mysyshynlabs.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False