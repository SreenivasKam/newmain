from flask import Blueprint, render_template, request, flash, url_for, redirect
from flask_mysqldb import MySQL
from projectfolder import app
from projectfolder import mysql,session_info
from datetime import datetime

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
            if(data[3] == password):
                current_time = datetime.now()
                current = current_time.strftime("%Y-%m-%d %H:%M:%S")
                data = 'insert into session_table (user_id,entry) values(' + str(int(data[0])) + ",'" +current +"');"
                cur.execute(data)
                mysql.connection.commit()
                session_info['loggedin'] = True
                session_info['id'] = data[0]
                session_info['username'] = data[1]
                return redirect(url_for('demand.demander'))
                # return render_template('check.html',msg = data)
            else:
                flash("Wrong password",'error')
                return redirect(url_for('core.login'))
        flash('No account found! Trying Signing Up','error')
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
        o = "insert into user_table (User_name,Email,User_password) values ('" + name + "','" + email + "','" + password + "');"
        cur.execute(o)
        flash("Account created. Please login",'success')
        mysql.connection.commit()
        return redirect(url_for('core.login'))

@core.route('/forgot')
def forgot():
    return render_template('check.html',msg ="This is forgot",link='/')