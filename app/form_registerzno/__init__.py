from flask import Blueprint, render_template, flash, session, redirect, url_for
from .forms import RegisterDoc
import json
from .getFunction import getFooterData, write_to_json, validation

registerzno_blueprint = Blueprint('registerzno', __name__, template_folder="templates/form_registerzno")

# LAB 5 ---------------------------------------------------------------------------------------------------------------------------------------------------------
@registerzno_blueprint.route('/registerForm', methods=['GET', 'POST'])
def formRegisterDoc():
    form = RegisterDoc()
    validation(form)
    if form.validate_on_submit():
        session['email'] = form.email.data
        if write_to_json(form):
            flash('Форма надіслана успішно! Дані успішно записані у json файл!', category='success')
        else:
            flash('Error', category='error')
        return redirect(url_for('registerzno.formRegisterDoc'))

    try:
        sesiya = session['email']
        with open('MysyshynDB.json') as f:
            data_files = json.load(f)
        form.email.data = sesiya
        form.e_number.data = data_files[sesiya]['e_number']
        form.e_pin.data = data_files[sesiya]['e_pin']
        form.e_year.data = data_files[sesiya]['e_year']
        form.d_series.data = data_files[sesiya]['d_series']
        form.d_number.data = data_files[sesiya]['d_number']
    except:
        return render_template("registerForm.html", form=form, data=getFooterData())

    return render_template("registerForm.html", form=form, data=getFooterData())

