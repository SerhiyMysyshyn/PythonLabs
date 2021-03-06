import enum
from sqlalchemy.types import Enum
from .. import db, bcrypt, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.png')
    password = db.Column(db.String(60), nullable=False)
    about_me = db.Column(db.Text, nullable=True)
    last_date = db.Column(db.DateTime, default=db.func.now())

    songs = db.relationship('Songs', backref='author_song', lazy=True)

    def __init__(self, username, email, password, about_me='', image_file='default.png'):
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
        self.about_me = about_me
        self.image_file = image_file

    def verify_password(self, pwd):
        return bcrypt.check_password_hash(self.password, pwd)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.password}')"