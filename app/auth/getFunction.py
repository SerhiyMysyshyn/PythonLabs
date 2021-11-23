from flask import request, current_app
from datetime import datetime
import os
import sys
import platform
import secrets
from PIL import Image

def getFooterData():
    OS_info = os.name + " " + platform.system() + " " + platform.release()
    current_datetime = datetime.now()
    userAgent = request.headers.get('User-Agent')
    pythonVersion = sys.version
    return [OS_info, pythonVersion, userAgent, current_datetime]

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
    output_size = (250, 250)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn
