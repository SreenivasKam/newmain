from flask import Blueprint, render_template,request
from flask_mysqldb import MySQL
from projectfolder import app
from projectfolder.demand.views import mysql
from datetime import datetime

resume = Blueprint('resume', __name__)


@resume.route('/resume')
def resumer():
    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'emp_profiles';")
    header = list(cur.fetchall())
    return render_template('resume.html', user=header)


@resume.route('/add_data_resume')
def add_data_resume():
    nothis= ['record_creation','last_updated_date','last_updated_by']
    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'emp_profiles';")
    header = list(cur.fetchall())
    cur.execute(
        "SELECT DISTINCT(type_) FROM legend")
    count = list(cur.fetchall())
    cur.execute(
        "SELECT * FROM legend")
    tabledata = list(cur.fetchall())
    data =[]
    for ele in count:
        data.append(ele[0])
    return render_template('add_data_resume.html', user=header,count=data,tabledata = tabledata,nothis=nothis)
    #return render_template('check.html',msg=nothis,count=data)

@resume.route('/writeresume', methods=['GET','POST'])
def writeresume():
    pass