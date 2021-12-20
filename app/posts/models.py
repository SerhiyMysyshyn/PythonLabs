import enum

from .. import db
# from sqlalchemy.types import Enum


post_tags_identifier = db.Table(
    'post_tags_identifier',
    db.Column('tags', db.Integer, db.ForeignKey('tag.id')),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'))
)

class PostType(enum.Enum):
    News = 'News'
    Publication = 'Publication'
    Other = 'Other'

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    posts = db.relationship("Post", back_populates="category")


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    image = db.Column(db.String(20), nullable=False, default='default_post.png')
    created = db.Column(db.DateTime, default=db.func.now())
    is_enabled = db.Column(db.Boolean, default=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    tags = db.relationship("Tag", secondary=post_tags_identifier)
    category = db.relationship("Category", back_populates="posts")

db.create_all()