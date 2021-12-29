from flask import Flask, g, request, jsonify
from functools import wraps
from ..posts.models import Category
from .. import db

from . import api_blueprint

api_username = 'admin'
api_password = 'admin'

def protected(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if auth and auth.username == api_username and auth.password == api_password:
            return f(*args, **kwargs)
        return jsonify({'message': 'Authentication failed!'}), 403
    return decorated

@api_blueprint.route('/categories', methods=['GET'])
@protected
def get_categories():
    categories = Category.query.all()
    return_values = [{"id": category.id, "name": category.name} for category in categories]

    return jsonify({'categories': return_values})

@api_blueprint.route('/category/<int:id>', methods=['GET'])
@protected
def get_category(id):
    category = Category.query.get_or_404(id)
    return jsonify({"id": category.id, "name": category.name})

@api_blueprint.route('/category', methods=['POST'])
def add_category():
    new_category_data = request.get_json()
    category = Category.query.filter_by(name=new_category_data['name']).first()

    if category:
        return jsonify({"Message": "Category already exist"})

    category = Category(name=new_category_data['name'])
    db.session.add(category)
    db.session.commit()
    return jsonify({"id": category.id, "name": category.name})


@api_blueprint.route('/category/<int:id>', methods=['PUT', 'PATCH'])
@protected
def edit_category(id):
    category = Category.query.get(id)
    if not category:
        return jsonify({"Message": "Category does not exist"})

    update_category_data = request.get_json()
    categories = Category.query.filter_by(name=update_category_data['name']).first()
    if categories:
        return jsonify({"Message": "Category already exist"})

    category.name = update_category_data['name']
    db.session.add(category)
    db.session.commit()

    return jsonify({"id": category.id, "name": category.name})


@api_blueprint.route('/category/<int:id>', methods=['DELETE'])
@protected
def delete_category(id):
    category = Category.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()

    return jsonify({'Message': 'The category has been deleted!'})