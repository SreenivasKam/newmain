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
        "SHOW COLUMNS FROM emp_profiles;")
    header = list(cur.fetchall())
    cur.execute(
        "Select * FROM emp_profiles;")
    data = list(cur.fetchall())
    return render_template('resume.html', user=header,data=data,filter=0)


@resume.route('/add_data_resume')
def add_data_resume():
    nothis= ['record_creation','last_updated_date','last_updated_by']
    cur = mysql.connection.cursor()
    cur.execute(
        "SHOW COLUMNS FROM emp_profiles;")
    header = list(cur.fetchall())
    cur.execute(
        "Select * FROM  resume_comments;")
    verify = list(cur.fetchall())
    cur.execute(
        "Select * FROM  hiring_legends;")
    tabledata = list(cur.fetchall())
    count = ['cdo_tower_status']
    return render_template('add_data_resume.html', verify=list(verify),user=header,count=count,tabledata = tabledata,nothis=nothis)
    #return render_template('check.html',msg=nothis,count=data)

@resume.route('/writeresume', methods=['GET','POST'])
def writeresume():
    msg = ' '
    cur = mysql.connection.cursor()
    cur.execute(
        "SHOW COLUMNS FROM emp_profiles;")
    header = list(cur.fetchall())
    # applying empty validation
    dict1 = {}
    t = []
    m = []
    nothis = ['record_creation_date', 'last_updated_date', 'last_updated_by']
    logs =['unique_id','cdo_tower_status']
    if request.method == 'POST':
        # passing HTML form data into python variable
        g = ''
        for i in range(len(header)-3):
            s = str(header[i][0]).lower()
            t.append(request.form.get(s, False))
            if(s in logs):
                m.append(request.form.get(s, False))
            g = g+'%s,'
            dict1[header[i][0].lower()] = request.form.get(s, False)

        for ele in nothis:
            g = g+'%s,'
            now = datetime.now()
            dt_string = now.strftime("%Y-%m-%d")
            t.append(dt_string)
        t = t[:-1]
        comments = 'Created new Resume added.'
        current_time = datetime.now()  
        m.append(comments)
        m.append(current_time.strftime("%Y-%m-%d %H:%M:%S"))
        m = str(m)
        m = m[1:-1]
        t.append("Sreenivas")
        g = g[:len(g)-1]
        o = 'INSERT INTO resume_logs VALUES (' + m +');'
        cur.execute('INSERT INTO emp_profiles VALUES ('+g+')', tuple(t))
        cur.execute(o)
        mysql.connection.commit()
        # displaying message
        msg = 'Data has been added to the database'
        link='/resume'
    return render_template('check.html', msg=msg,link=link)


@resume.route('/filter_resume')
def filter_resume():
    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT * FROM hiring_legends ;")
    count = list(cur.fetchall())
    return render_template("filter_resume.html",count=count)

@resume.route('/resumefil', methods=['GET', 'POST'])
def resumefil():
    msg = 'Ok'
    cur = mysql.connection.cursor()
    cur.execute(
        "SHOW COLUMNS FROM emp_profiles;")
    header = list(cur.fetchall())
    cur.execute(
        "SELECT value_ FROM hiring_legends;")
    count = list(cur.fetchall())
    t=[]
    dict1 ={}
    if request.method == 'POST':
        for i in range(len(count)):
            s = str(count[i][0])
            if(request.form.get(s, False)!=False):
               t.append(request.form.get(s, False))
        cur = mysql.connection.cursor()
        b = str(t)
        b = b[1:-1]
        p='select * from emp_profiles where cdo_tower_status in (' + b+ ');'
        cur.execute(p)
        count1 = list(cur.fetchall())
    #return render_template('check.html',msg = p)
    return render_template('resume.html', user=header, data=count1,filter=1)