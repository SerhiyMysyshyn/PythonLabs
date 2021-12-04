from flask import request, current_app
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
