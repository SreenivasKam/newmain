from flask import Blueprint, render_template, request, flash, url_for, redirect
from flask_mysqldb import MySQL
from projectfolder import app, mysql,session_info
from datetime import datetime

settings = Blueprint('settings', __name__)
# session_info['loggedin'] = True
# session_info['id'] = 1

@settings.route('/settings')
def setting():
   groupList = ['Managers','Master Admin','Tech SPOCs','Staffing Team']
   if session_info['loggedin']:
      cur = mysql.connection.cursor()
      fetchUserData = "select * from user_table where user_id = " + str(session_info['id']) + ";"
      cur.execute(fetchUserData)
      userData = cur.fetchone()
      fetchGroupData = "select * from access_table where user_id = " + str(session_info['id']) + ";"
      cur.execute(fetchGroupData)
      groupData = cur.fetchone()
      name =  userData[1]
      email =  userData[2]
      groupName= str(groupList[groupData[1]-1])
      skill = groupData[3]
      titles = ['Name','Email','Access Name','Skill']
      sendData = (name,email,groupName,skill)
      return render_template('settings.html',titles = titles,sendData =sendData)
      # return render_template('settings.html',msg = fetchUserData,msg1 = fetchGroupData)