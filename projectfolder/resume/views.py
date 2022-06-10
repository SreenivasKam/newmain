from flask import Blueprint,session, render_template,request, request ,flash,url_for,redirect
from flask_mysqldb import MySQL
from projectfolder import app
import random
from projectfolder import mysql
from projectfolder.core.views import connect
from datetime import datetime

resume = Blueprint('resume', __name__)


@resume.route('/resume')
def resumer():
    cur = mysql.connection.cursor()
    cur.execute(
        "Select type_ from resume_comments;")
    header = list(cur.fetchall())
    cur.execute(
        "Select * FROM emp_profiles;")
    data = list(cur.fetchall())
    mysql.connection.commit()
    return render_template('resume.html', user=header,data=data,filter=0,session_info=session)
    # return render_template('check.html',msg = connect.session_info['groupno'])
@resume.route('/resume2')
def resumer2():
    cur = mysql.connection.cursor()
    cur.execute(
        "Select * FROM  hiring_legends;")
    tabledata = list(cur.fetchall())
    cur.execute(
        "Select type_ from resume_comments;")
    header = list(cur.fetchall())
    cur.execute(
        "(select position_id,demand_id from resumemapping where user_id =" + str(session['id']) + ");")
    data1 = list(cur.fetchall())
    d1 = {}
    for p in data1:
        if(p[1] in d1.keys()):
            d1[p[1]].append(p[0])
        else:
            d1[p[1]] = []
            d1[p[1]].append(p[0])
    x =  list(d1.values())
    k = ['0']+[j for i in x for j in i]
    k = str(k)
    k = k[1:-1]
    l = "Select * FROM emp_profiles where position_id in (" +k+");"
    cur.execute(l)
    data = list(cur.fetchall())
    mysql.connection.commit()
    return render_template('resume2.html', dict1 = d1,tabledata =tabledata ,user=header,data=data,filter=0,session_info=session)
    # return render_template('check.html',msg =d1)

@resume.route('/add_data_resume')
def add_data_resume():
    nothis= ['record_creation','last_updated_date','last_updated_by']
    cur = mysql.connection.cursor()
    cur.execute(
        "SHOW COLUMNS FROM emp_profiles;")
    header = list(cur.fetchall())
    cur.execute(
        "select type_ from resume_comments;")
    head = list(cur.fetchall())
    cur.execute(
        "Select * FROM  resume_comments;")
    verify = list(cur.fetchall())
    cur.execute(
        "Select * FROM  hiring_legends;")
    tabledata = list(cur.fetchall())
    cur.execute(
        "Select id FROM  demands where status = 'Open'")
    jdData = list(cur.fetchall())
    count = ['cdo_tower_status','linking_jd']
    cur.close()
    return render_template('add_data_resume.html', verify=list(verify),head=head,jdData = jdData,user=header,count=count,tabledata = tabledata,nothis=nothis)
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
    id = random.randint(3,999999)
    t.append(id)
    m.append(id)
    nothis = ['record_creation_date', 'last_updated_date', 'last_updated_by']
    logs =['position_id','cdo_tower_status']
    jd = ['linking_jd']
    if request.method == 'POST':
        # passing HTML form data into python variable
        g = ''
        for i in range(1,len(header)-3):
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
        t.append(session['username'])
        g = g[:len(g)-1]
        t = str(t)
        t = t[1:-1]
        p= 'INSERT INTO emp_profiles VALUES ('+t+');'
        o = 'INSERT INTO resume_logs VALUES (' + m +');'
        cur.execute(p)
        cur.execute(o)
        f = open("demofile3.txt", "a")
        f.write(p)
        f.write('\n')
        f.write(o)
        f.close()
        mysql.connection.commit()
        # displaying message
        msg = 'Data has been added to the database'
        flash(msg)
    return redirect(url_for('resume.resumer'))


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


@resume.route('/updated/<id>')
def updated(id):
    cur = mysql.connection.cursor()
    nothis= ['record_creation','last_updated_date','last_updated_by']
    p = "Select * from emp_profiles where position_id  ="+id+";"
    cur.execute(p)
    sendata = list(cur.fetchall())
    cur = mysql.connection.cursor()
    cur.execute(
        "SHOW COLUMNS FROM emp_profiles;")
    header = list(cur.fetchall())
    cur.execute(
        "Select type_ from resume_comments;")
    header2 = list(cur.fetchall())
    cur.execute(
        "Select * FROM  resume_comments;")
    verify = list(cur.fetchall())
    cur.execute(
        "Select * FROM  hiring_legends;")
    tabledata = list(cur.fetchall())
    count = ['cdo_tower_status']
    return render_template('updating_resume.html', header2=header2,msg=sendata,verify=list(verify),user=header,count=count,tabledata = tabledata,nothis=nothis)

@resume.route('/changesresume', methods=['GET','POST'])
def changesresume():
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
    logs =['position_id','cdo_tower_status']
    if request.method == 'POST':
        # passing HTML form data into python variable
        p = 'update emp_profiles set '
        for i in range(len(header)-3):
            s = str(header[i][0]).lower()
            if(i==0):
                id=str(request.form.get(s, False))
            else:
                df = str(request.form.get(s, False))
                df = df.replace("'", "-")
                p = str(p)+ s + " = '" +df + "', "
            if(s in logs):
                m.append(request.form.get(s, False))

        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%d")
        p = p+" last_updated_date = '" + dt_string + "', "
        p = p+" last_updated_by = '"+ session['username'] + "'where position_id = '" + id +"' ;"

        comments = request.form.get("update_resume_comments", False)
        current_time = datetime.now()  
        m.append(comments)
        m.append(current_time.strftime("%Y-%m-%d %H:%M:%S"))
        m[0] = int(id)
        m = str(m)
        m = m[1:-1]
        o = 'INSERT INTO resume_logs VALUES (' + m +');'
        # return render_template('check.html',msg = p)
        #cur.execute('INSERT INTO emp_profiles VALUES ('+g+')', tuple(t))
        cur.execute(o)
        cur.execute(p)
        mysql.connection.commit()
        # displaying message
        msg = 'Data has been updated'
        flash(msg)
    return redirect(url_for('resume.resumer'))
@resume.route('/deleted/<id>')
def deleted(id):
    f = "delete from resume_logs where position_id = '" + id + "';"
    p = "delete from emp_profiles where position_id = '" + id + "';"
    cur = mysql.connection.cursor()
    current_time = datetime.now()
    new = current_time.strftime("%Y-%m-%d %H:%M:%S")
    id = "Removed ID: " + id
    m= [111,id]
    comments = "This data has been exhausted"
    current_time = datetime.now()
    m.append(comments)
    m.append(current_time.strftime("%Y-%m-%d %H:%M:%S"))
    m = str(m)
    m = m[1:-1]
    o = 'INSERT INTO resume_logs VALUES (' + m + ');'
    cur.execute(f)
    cur.execute(o)
    cur.execute(p)
    mysql.connection.commit()
    msg = " This Record is successfully deleted"
    flash(msg)
    return redirect(url_for('resume.resumer'))

@resume.route('/filter_resumelogs')
def fresumelogs():
    cur = mysql.connection.cursor()
    cur.execute(
        "SHOW COLUMNS FROM resume_logs;")
    header = list(cur.fetchall())
    return render_template('logs_filter.html',header=header,value=2)

@resume.route('/filter_resume_logs_push_back', methods=['GET','POST'])
def filterLogsPushBack():
    value = ''
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        field = request.form.get('field', False)
        type = request.form.get('type', False)
        textbox = request.form.get('textbox', False)
        if(type == 'starts'):
            value = " LIKE '" + str(textbox) + "%'"
        elif(type == 'equal'):
            value = " =  '" + str(textbox) + "'" 
        else:
            s = str(list(textbox.split(",")))
            s =s[1:-1]
            value = " in (" + str(s) + ")" 
        o = "select * from resume_logs where " + str(field) + " " + str(value) + " ;"
        cur.execute(o)
        data1 = cur.fetchall()
        cur = mysql.connection.cursor()
        cur.execute(
        "SHOW COLUMNS FROM data_logs;")
        header = (cur.fetchall())
        cur.execute("SELECT * from data_logs order by date_updated desc limit 10;")
        data = list(cur.fetchall())
        cur.execute(
        "SHOW COLUMNS FROM resume_logs;")
        header1 = (cur.fetchall())
        return render_template('logs.html', user=header, data=data, user1=header1, data1=data1,showresume=10,session_info=session)

@resume.route('/viewjd', methods=['GET','POST'])
def viewjd():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        field = request.form.get('field', False)
    return render_template('check.html',p=0)

@resume.route('/contact', methods=['GET','POST'])
def contact():
    if request.method == 'POST':
        if request.form.get('field', False):
            cur = mysql.connection.cursor()
            field = request.form.get('field', False)
            cur.execute(
            "SHOW COLUMNS FROM demands;")
            header = (cur.fetchall())
            cur.execute("select * from demands where id = '" + str(field) + "';")
            sendData = cur.fetchone()
            return render_template('viewjd.html',titles=header,sendData=sendData)


@resume.route('/reject')
def reject():
    pass

@resume.route('/selected')
def selected():
    pass


@resume.route('/viewjd/<key1>')
def viewedjd(key1):
    cur = mysql.connection.cursor()
    cur.execute(
    "SHOW COLUMNS FROM demands;")
    header = (cur.fetchall())
    cur.execute("select * from demands where id = '" + str(key1) + "';")
    sendData = cur.fetchone()
    return render_template('viewjd.html',titles=header,sendData=sendData)

