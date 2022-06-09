from flask import Blueprint,session, render_template, request, flash, url_for, redirect
from flask_mysqldb import MySQL
from projectfolder import app, mysql
from projectfolder.core.views import connect
from datetime import datetime

settings = Blueprint('settings', __name__)

@settings.route('/settings')
def setting():
   groupList = ['Manager','Master Admin','Tech SPOCs','Staffing Team']
   if session['loggedin']:
      cur = mysql.connection.cursor()
      fetchUserData = "select * from user_table where user_id = " + str(session['id']) + ";"
      cur.execute(fetchUserData)
      userData = cur.fetchone()
      fetchGroupData = "select * from access_table where user_id = " + str(session['id']) + ";"
      cur.execute(fetchGroupData)
      groupData = cur.fetchone()
      name =  userData[1]
      email =  userData[2]
      groupName= str(groupList[groupData[1]-1])
      skill = groupData[3]
      titles = ['Name','Email','Access Name','Skill']
      sendData = (name,email,groupName,skill)
      value = 0
      return render_template('settings.html',titles = titles,sendData =sendData,session_info=session,elementValue = value)
      # return render_template('settings.html',msg = fetchUserData,msg1 = fetchGroupData)

@settings.route('/manageaccess')
def manageaccess():
      cur = mysql.connection.cursor()
      tableHead = ['Select','Name','Email','Group','Skill']
      groupList = ['Manager','Master Admin','Tech SPOCs','Staffing Team']
      skills = ['Databricks','Python','Pyspark']
      fetchUserData = "select * from user_table where skills = 'Empty'"
      cur.execute(fetchUserData)
      accessData = cur.fetchall()
      return render_template('settings.html',accessdata = list(accessData),tableHead =tableHead,groupList = groupList,skills = skills,elementValue = 1,session_info=session)

@settings.route('/managelegend')
def managelegend():
   cur =mysql.connection.cursor()
   types="select distinct type_ from legend "
   cur.execute(types)
   typeData=cur.fetchall()
   return render_template('settings.html',typedata=list(typeData),elementValue = 2,session_info=session)


@settings.route('/pushdata', methods=['GET', 'POST'])
def pushData():
   groupList = ['Manager','Master Admin','Tech SPOCs','Staffing Team']
   cur = mysql.connection.cursor()
   fetchUserData = "select * from user_table where skills = 'Empty'"
   cur.execute(fetchUserData)
   accessData = cur.fetchall()
   for i in range(len(accessData)):
      id = request.form.get(str(accessData[i][0]), False)
      if(id!='on'):
         continue
      group = request.form.get('group'+str(accessData[i][0]), False)
      value = groupList.index(str(group)) +1 
      skill = request.form.get('skill'+str(accessData[i][0]), False)
      updateVariable = "Update user_table set skills = '"+ skill + "' where user_id = " + str(accessData[i][0])+ " ;"
      insertVariable  = "insert into access_table (groupid,user_id,skills) values ("+str(value) + ","  + str(accessData[i][0]) + ",'" + str(skill) +"');"
      cur.execute(updateVariable)
      cur.execute(insertVariable)
      f = open("demofile4.txt", "a")
      f.write(updateVariable)
      f.write('\n')
      f.write(insertVariable )
      f.write('\n')
      f.close()
   mysql.connection.commit()
   flash('User approved','success')
   return redirect(url_for('settings.manageaccess'))

@settings.route('/pushdata1', methods=['GET', 'POST'])
def pushData1():
   cur =mysql.connection.cursor()
   types="select distinct type_ from legend "
   cur.execute(types)
   typeData=cur.fetchall()
   if request.method == 'POST':
        name = request.form.get('field', False)
        val = request.form.get('val', False)
        o = "insert into legend (type_,value_) values ('" + name + "','" + val + "');"
        cur.execute(o)
        mysql.connection.commit()
   flash('Legend Successfully added to Database','success')
   return redirect(url_for('settings.managelegend'))

@settings.route('/viewusers')
def viewusers():
   cur =mysql.connection.cursor()
   cur.execute(
        "SHOW COLUMNS FROM user_table;")
   header = ['User Id','User Name','Email','Skills']
   types="select user_id,user_name,email,skills from user_table where user_id <> 1"
   cur.execute(types)
   typeData=cur.fetchall()
   return render_template('settings.html',header=header,typeData=typeData,elementValue = 3,session_info=session)