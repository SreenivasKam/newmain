from flask import Blueprint, render_template, request
from flask_mysqldb import MySQL
from projectfolder import app
from datetime import datetime

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'sree9078'
app.config['MYSQL_DB'] = 'project'


mysql = MySQL(app)
demand = Blueprint('demand', __name__)


@demand.route('/')
def demander():
    cur = mysql.connection.cursor()
    cur.execute(
        "SHOW COLUMNS FROM demands;")
    header = (cur.fetchall())
    cur.execute("SELECT * from demands;")
    data = list(cur.fetchall())
    return render_template('demand.html', user=header, data=data, filter=0)


@demand.route('/add_data')
def add_data():
    nothis = ['record_creation_date', 'last_updated_date', 'last_updated_by']
    cur = mysql.connection.cursor()
    cur.execute(
        "SHOW COLUMNS FROM demands;")
    header = list(cur.fetchall())
    cur.execute(
        "Select * FROM demand_comments;")
    verify = list(cur.fetchall())
    cur.execute(
        "SELECT DISTINCT(type_) FROM legend")
    count = list(cur.fetchall())
    cur.execute(
        "SELECT * FROM legend")
    tabledata = list(cur.fetchall())
    data = []
    for ele in count:
        data.append(ele[0])
    return render_template('add_data.html', verify=list(verify), user=header, count=data, tabledata=tabledata, nothis=nothis)
    # return render_template('check.html',msg=nothis,count=data)


@demand.route('/filter')
def filter():
    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT * FROM legend where type_ in ('status','primary_jrss','position_type')")
    count = list(cur.fetchall())
    return render_template('filter.html', count=count)


@demand.route('/demandfil', methods=['GET', 'POST'])
def demandfil():
    msg = 'Ok'
    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT * FROM legend where type_ in ('status','primary_jrss','position_type')")
    count = list(cur.fetchall())
    t = ['New']
    cur.execute(
        "SHOW COLUMNS FROM demands;")
    header = (cur.fetchall())
    g = ' '
    dict1 = {}
    if request.method == 'POST':
        for i in range(len(count)):
            d = str(count[i][0])
            s = str(count[i][1])
            if(request.form.get(s, False) != False):
                if(d not in dict1.keys()):
                    dict1[d] = []
                dict1[d].append(request.form.get(s, False))
        cur = mysql.connection.cursor()
        p = 'select * from demands where'
        for i in dict1.keys():
            k = str((dict1[i]))
            k = k[1:]
            k = k[:-1]
            p = p + " " + str(i) + ' in (' + k + ") or"
        p = p[:-2]
        p = p+";"
        cur.execute(p)
        count1 = list(cur.fetchall())
    # return render_template('check.html',msg = p)
    return render_template('demand.html', user=header, data=count1, filter=1)


@demand.route('/writedemand', methods=['GET', 'POST'])
def writedemand():
    msg = ' '
    cur = mysql.connection.cursor()
    cur.execute(
        "SHOW COLUMNS FROM demands;")
    header = list(cur.fetchall())
    # applying empty validation
    dict1 = {}
    t = []
    m = []
    nothis = ['record_creation_date', 'last_updated_date', 'last_updated_by']
    logs = ['id', 'status', 'sub_status']
    if request.method == 'POST':
        # passing HTML form data into python variable
        g = ''
        for i in range(len(header)-3):
            s = str(header[i][0]).lower()
            if(s in logs):
                m.append(request.form.get(s, False))
            t.append(request.form.get(s, False))
            g = g+'%s,'
            dict1[header[i][0].lower()] = request.form.get(s, False)

        for ele in nothis:
            g = g+'%s,'
            now = datetime.now()
            dt_string = now.strftime("%Y-%m-%d")
            t.append(dt_string)
        comments = 'Created new Job demand.'
        current_time = datetime.now()
        m.append(comments)
        m.append(current_time.strftime("%Y-%m-%d %H:%M:%S"))
        m = str(m)
        m = m[1:-1]
        t = t[:-1]
        t.append("Sreenivas")
        g = g[:len(g)-1]
        o = 'INSERT INTO data_logs VALUES (' + m + ');'
        cur.execute('INSERT INTO demands VALUES ('+g+')', tuple(t))
        cur.execute(o)
        mysql.connection.commit()
        # displaying message
        msg = 'Data has been added to the database'
        link = '/'
    return render_template('check.html', msg=msg, link=link)


@demand.route('/logs')
def logs():
    cur = mysql.connection.cursor()
    cur.execute(
        "SHOW COLUMNS FROM data_logs;")
    header = (cur.fetchall())
    cur.execute("SELECT * from data_logs;")
    data = list(cur.fetchall())
    cur.execute(
        "SHOW COLUMNS FROM resume_logs;")
    header1 = (cur.fetchall())
    cur.execute("SELECT * from resume_logs;")
    data1 = list(cur.fetchall())
    return render_template('logs.html', user=header, data=data, user1=header1, data1=data1)


@demand.route('/updates/<id>')
def updates(id):
    cur = mysql.connection.cursor()
    p = "Select * from demands where ID ='"+id+"';"
    cur.execute(p)
    sendata = list(cur.fetchall())
    nothis = ['record_creation_date', 'last_updated_date', 'last_updated_by']
    cur = mysql.connection.cursor()
    cur.execute(
        "SHOW COLUMNS FROM demands;")
    header = list(cur.fetchall())
    cur.execute(
        "Select * FROM demand_comments;")
    verify = list(cur.fetchall())
    cur.execute(
        "SELECT DISTINCT(type_) FROM legend")
    count = list(cur.fetchall())
    cur.execute(
        "SELECT * FROM legend")
    tabledata = list(cur.fetchall())
    data = []
    for ele in count:
        data.append(ele[0])
    #return render_template('check.html',msg = sendata)
    return render_template('updating.html',msg=sendata,verify=list(verify), user=header, count=data, tabledata=tabledata, nothis=nothis)

@demand.route('/changes',methods=['GET', 'POST'])
def changes():
    msg = ' '
    cur = mysql.connection.cursor()
    cur.execute(
        "SHOW COLUMNS FROM demands;")
    header = list(cur.fetchall())
    # applying empty validation
    dict1 = {}
    t = []
    m = []
    nothis = ['record_creation_date', 'last_updated_date', 'last_updated_by']
    logs = ['id', 'status', 'sub_status']
    if request.method == 'POST':
        # passing HTML form data into python variable
        p = 'update demands set '
        for i in range(len(header)-3):
            s = str(header[i][0]).lower()
            if(i==0):
                id=str(request.form.get(s, False))
            else:
                p = str(p)+ s + " = '" + str(request.form.get(s, False))+ "', "
            if(s in logs):
                m.append(request.form.get(s, False))

        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%d")
        t.append(dt_string)
        p = p+" last_updated_date = '" + dt_string + "', "
        p = p+" last_updated_by = 'Sreenivas' where ID = '" + id +"' ;"

        comments = request.form.get("update_comments", False)
        current_time = datetime.now()
        m.append(comments)
        m.append(current_time.strftime("%Y-%m-%d %H:%M:%S"))
        m = str(m)
        m = m[1:-1]
        o = 'INSERT INTO data_logs VALUES (' + m + ');'
        cur.execute(p)
        cur.execute(o)
        mysql.connection.commit()
        # displaying message
        msg = 'Data has been updated successfully'
        link = '/'
    return render_template('check.html', msg=msg,link=link)
    #return render_template('check.html',msg = 'this works bro')

@demand.route('/delete/<id>')
def delete(id):
    f = "delete from data_logs where unique_id = '" + id + "';"
    p = "delete from demands where ID = '" + id + "';"
    cur = mysql.connection.cursor()
    current_time = datetime.now()
    new = current_time.strftime("%Y-%m-%d %H:%M:%S")
    id = "Removed ID: " + id
    m= ['admin','Deleted',id]
    comments = "This data has been exhausted"
    current_time = datetime.now()
    m.append(comments)
    m.append(current_time.strftime("%Y-%m-%d %H:%M:%S"))
    m = str(m)
    m = m[1:-1]
    o = 'INSERT INTO data_logs VALUES (' + m + ');'
    cur.execute(f)
    cur.execute(o)
    cur.execute(p)
    mysql.connection.commit()
    msg = " This Record is successfully deleted"
    return render_template("check.html",msg= msg)