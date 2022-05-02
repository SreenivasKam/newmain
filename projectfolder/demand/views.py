from flask import Blueprint, render_template,request
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
    return render_template('demand.html', user=header, data=data)


@demand.route('/add_data')
def add_data():
    nothis= ['record_creation_date','last_updated_date','last_updated_by']
    cur = mysql.connection.cursor()
    cur.execute(
        "SHOW COLUMNS FROM demands;")
    header = list(cur.fetchall())
    cur.execute(
        "Select * FROM demand_comments;")
    verify= list(cur.fetchall())
    cur.execute(
        "SELECT DISTINCT(type_) FROM legend")
    count = list(cur.fetchall())
    cur.execute(
        "SELECT * FROM legend")
    tabledata = list(cur.fetchall())
    data =[]
    for ele in count:
        data.append(ele[0])
    return render_template('add_data.html',verify=list(verify),user=header,count=data,tabledata = tabledata,nothis=nothis)
    #return render_template('check.html',msg=nothis,count=data)

@demand.route('/filter')
def filter():
    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT * FROM legend")
    count = list(cur.fetchall())
    return render_template('filter.html',count=count)

@demand.route('/projectfil', methods=['GET','POST'])
def projectfil():
    msg ='Ok'
    return render_template('check.html',msg=msg)

@demand.route('/writedemand', methods=['GET','POST'])
def writedemand():
    msg =' '
    cur = mysql.connection.cursor()
    cur.execute(
        "SHOW COLUMNS FROM demands;")
    header = list(cur.fetchall())
    # applying empty validation
    dict1 ={}
    t =[]
    nothis= ['record_creation_date','last_updated_date','last_updated_by']
    if request.method == 'POST':
        # passing HTML form data into python variable
        g =''
        for i in range(len(header)-3):
            s = str(header[i][0]).lower()
            t.append(request.form.get(s, False))
            g=g+'%s,'
            dict1[header[i][0].lower()] = request.form.get(s, False)
        
        for ele in nothis:
            g=g+'%s,'
            now = datetime.now()
            dt_string = now.strftime("%Y-%m-%d")
            t.append(dt_string)
        t = t[:-1]
        t.append("Sreenivas")
        g = g[:len(g)-1]
        cur.execute('INSERT INTO demands VALUES ('+g+')',tuple(t))
        mysql.connection.commit()
        # displaying message
        msg = 'Data has been added to the database'
    return render_template('check.html',msg=msg)
