from flask import Blueprint, render_template, request, flash, url_for, redirect
from flask_mysqldb import MySQL
from projectfolder import app
from projectfolder import mysql
from datetime import datetime
import cache

core = Blueprint('core', __name__)
@core.route('/')
def login():
    return render_template('login.html')

@core.route('/connect', methods=['GET', 'POST'])
def connect():
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        email = request.form.get('inputEmail', False)
        password = request.form.get('inputPassword', False)
        o = "select * from user_table where Email = '" + email + "' ;"
        cur.execute(o)
        data = cur.fetchone();
        if(data != None):
            if(data[3] == password and data[4]!='Empty'):
                current_time = datetime.now()
                current = current_time.strftime("%Y-%m-%d %H:%M:%S")
                data1 = 'insert into session_table  (user_id,user_name,entry,logged_info) values(' + str(int(data[0])) + ",'" +str(data[1]) + "','" +current +"','Y');"
                cur.execute(data1)
                data2 = "select * from access_table where user_id = " + str(data[0]) + ";"
                cur.execute(data2)
                groupData = cur.fetchone()
                mysql.connection.commit()
                # session_info['loggedin'] = True
                # session_info['id'] = data[0]
                # session_info['username'] = data[1]
                # session_info['groupno'] = int(groupData[1])
                session_info = {'loggedin':True,'id':data[0],'username':data[1],'groupno':int(groupData[1])}
                connect.session_info =  session_info
                cur.close()
                # return render_template('demand.html',sessionData = session_info)
                return redirect(url_for('demand.demander',sessionData= str(session_info)))
                #return render_template('check.html',msg = int(groupData[1]))
            else:
                if(data[4]=='Empty'):
                    flash("Please wait until Admin approves",'error')
                    return redirect(url_for('core.login'))
                else:
                    flash("Wrong password",'error')
                    cur.close()
                    return redirect(url_for('core.login'))
        flash('No account found! Trying Signing Up','error')
        cur.close()
        return redirect(url_for('core.login'))

@core.route('/signup')
def signup():
    return render_template('signup.html')

@core.route('/signupdata', methods=['GET', 'POST'])
def signupdata():
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        name = request.form.get('name', False)
        email = request.form.get('inputEmail', False)
        password = request.form.get('inputPassword', False)
        o = "insert into user_table (user_name,email,user_password,skills) values ('" + name + "','" + email + "','" + password + "','Empty');"
        p = "select * from user_table where Email = '" + email + "' ;"
        cur.execute(p)
        p = cur.fetchone()
        if(p==None):
            cur.execute(o)
            flash("Account created. Please login after the admin approves",'success')
        else:
            flash("Email Id already used! Please Login",'error')
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('core.login'))

@core.route('/forgot')
def forgot():
    return render_template('check.html',msg ="This is forgot",link='/')

@core.route('/logout')
def logout():
    try:
      if session_info['loggedin']:
         pass
    except:
      cur = mysql.connection.cursor()
      cur.execute("select * from session_table order by entry desc limit 1;")
      data = cur.fetchone()
      if(data[4] != 'N'):
         session_info = {}
         session_info['loggedin'] = True
         session_info['id'] = data[1]
         session_info['username'] = data[2]  
    finally:
        current_time = datetime.now()
        current = current_time.strftime("%Y-%m-%d %H:%M:%S")
        data1 = 'insert into session_table  (user_id,user_name,entry,logged_info) values(' + str(int(session_info['id'])) + ",'" +str(session_info['username']) + "','" +current +"','N');"
        cur.execute(data1)
        flash('Logged out successfully','success')
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('core.login'))
        #return render_template('check.html',msg=data1)
