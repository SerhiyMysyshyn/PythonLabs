from flask import render_template, Blueprint
from flask import current_app as app
from app.getAdditionalData import *
from app.getFunction import getFooterData

main_bp = Blueprint('main_bp', __name__, template_folder="templates/main_bp")

@main_bp.route('/')
def home():
    return render_template('home.html', data=getFooterData())

@main_bp.route('/about/')
def about():
    return render_template('about.html', data=getFooterData(), skills=skills)

@main_bp.route('/myworks/')
def myworks():
    return render_template('myworks.html', data=getFooterData(), projectsData=projectsData)

@main_bp.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', data=getFooterData())