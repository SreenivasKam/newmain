from flask import Blueprint, render_template, request, flash, url_for, redirect
from flask_mysqldb import MySQL
from projectfolder import app, mysql,session_info
from datetime import datetime

settings = Blueprint('settings', __name__)

@settings.route('/settings')
def setting():
   if session_info['loggedin']:
      return render_template('settings.html')