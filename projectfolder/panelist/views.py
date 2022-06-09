from flask import Blueprint, render_template, request, flash, url_for, redirect
from flask_mysqldb import MySQL
from projectfolder import app
from projectfolder import mysql
from datetime import datetime
import cache
from projectfolder.mlmodel.newcode import executetrige

panelist = Blueprint('panelist', __name__)
@panelist.route('/')
def viewpalist():
    return render_template('panelistscreen.html')