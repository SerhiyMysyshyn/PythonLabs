from wtforms.validators import Length, Regexp, InputRequired
import json
from app.errorList import *
from flask import request
from datetime import datetime
import os
import sys
import platform

def getFooterData():
    OS_info = os.name + " " + platform.system() + " " + platform.release()
    current_datetime = datetime.now()
    userAgent = request.headers.get('User-Agent')
    pythonVersion = sys.version
    return [OS_info, pythonVersion, userAgent, current_datetime]

def write_to_json(form):
    data = {
        form.email.data: {
            'password': form.password.data,
            'e_number': form.e_number.data,
            'e_pin': form.e_pin.data,
            'e_year': form.e_year.data,
            'd_series': form.d_series.data,
            'd_number': form.d_number.data,
        },
    }
    try:
        with open('MysyshynDB.json') as f:
            data_files = json.load(f)
            data_files.update(data)

            with open('MysyshynDB.json', 'w', encoding='utf-8') as f:
                json.dump(data_files, f, ensure_ascii=False, indent=4)
            return True
    except:
        with open('MysyshynDB.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            return False


def validation(form):
    if form.e_year.data is not None:
        regex = ''
        length = 0

        if int(form.e_year.data) < 2015:
            regex = '^[A-Z]{2}$'
            length = 8
        else:
            regex = '^[A-Z][0-9]{2}$'
            length = 6

        form.d_series.validators = [Regexp(regex=regex, message=error_8)]
        form.d_number.validators = [InputRequired(error_3), Length(min=length, max=length, message=error_9)]