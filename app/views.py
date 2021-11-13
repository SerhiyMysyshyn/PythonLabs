from flask import url_for, render_template, session, request, flash, redirect
from flask import current_app as app
from .getAdditionalData import *
from .getFunction import getFooterData


@app.route('/')
def home():
    return render_template('home.html', data=getFooterData())

@app.route('/about/')
def about():
    return render_template('about.html', data=getFooterData(), skills=skills)

@app.route('/myworks/')
def myworks():
    return render_template('myworks.html', data=getFooterData(), projectsData=projectsData)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', data=getFooterData())
