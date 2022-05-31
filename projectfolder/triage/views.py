from flask import Blueprint, render_template,request, request ,flash,url_for,redirect
from flask_mysqldb import MySQL
from projectfolder import app
from projectfolder import mysql
from projectfolder.core.views import connect
from datetime import datetime
from projectfolder.mlmodel.code import executeTriage

triage = Blueprint('triage', __name__)


@triage.route('/triage')
def triager():
    return render_template("mlmodel.html",msg = "this is triage")

@triage.route('/shorlist/<id>')
def shortlist(id):
    cur = mysql.connection.cursor()
    p = "Select preferred_Skills from demands where ID ='"+id+"';"
    cur.execute(p)
    fetchData = cur.fetchone()
    fetchData = list(fetchData[0].split(','))
    fetchpaths = "select box_link from emp_profiles"
    cur.execute(fetchpaths)
    paths = cur.fetchall()
    newdict = {}
    for ele in paths:
        newdict[ele[0]] = executeTriage(ele[0], fetchData)
    ##############
    #filter the dict with some percentage
    #fetch panelist from the user table for the skill required
    #table - which panelist for which resume

    cur.execute(
        "SHOW COLUMNS FROM emp_profiles;")
    header = list(cur.fetchall())
    cur.execute(
        "Select Unique_id,Cand_name,Jrss,Box_link FROM emp_profiles;")
    data = list(cur.fetchall())
    mysql.connection.commit()
    list1=['Unique_id','Cand_name','Jrss','Box_link']
    return render_template("mlmodel.html",user=header,data=data,list1=list1,msg = newdict)
    return render_template('check.html',msg = newdict)