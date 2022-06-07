from flask import Blueprint, render_template,request, request ,flash,url_for,redirect
from flask_mysqldb import MySQL
from projectfolder import app
from projectfolder import mysql
from projectfolder.core.views import connect
from datetime import datetime
from projectfolder.mlmodel.newcode import executetrige
from projectfolder.mlmodel.code import executeTriage

triage = Blueprint('triage', __name__)


@triage.route('/triage')
def triager():
    return render_template("mlmodel.html",msg = "this is triage")

@triage.route('/shorlist/<id>')
def shortlist(id):
    checknumber = 0
    f = 0
    qw =0
    cur = mysql.connection.cursor()
    p = "Select Skill_with_experience from demands where ID ='"+id+"';"
    cur.execute(p)
    fetchData = str(list(cur.fetchone()))
    fetchData = fetchData[2:-2]
    fetchpaths = "select * from emp_profiles"
    cur.execute(fetchpaths)
    paths = cur.fetchall()
    d1 = {}
    skill = fetchData.split(',')
    for ele in skill:
        k,v = ele.split('-')
        d1[k.lower()] = v
    skill = list(d1.keys())
    newdict = {}
    fetchpanelist = 'select user_id,skills from access_table where groupid = 3;'
    cur.execute(fetchpanelist)
    datafetched = cur.fetchall()
    for ele in paths:
        d=0
        checknumber=0
        result = executetrige(ele[8], fetchData)
        newdict[ele[1]] = result
        # return render_template('check.html',msg = paths)
        if(result=='Shortlisted'):
            cur.execute('select user_id from resumemapping ;')
            listuser1 = cur.fetchall()
            listuser = list(map(lambda x: x[0], listuser1))
            il = "select demand_id from resumemapping where unique_id = '" + str(ele[1])+"';"
            cur.execute(il)
            getdata = list(cur.fetchall())
            getfeed = list(map(lambda x: str(x[0]), getdata))
            # return render_template('check.html',msg = (id,getfeed))
            if(str(id) in getfeed):
                qw +=1
                continue
            else:
                if(listuser == []):
                    for i in datafetched:
                        # return render_template('check.html',msg =(i,i[0],i[1]) )
                        kf = list(str(i[1]).split(","))
                        k = list(map(lambda x: str(x).lower(), kf))
                        check = any(item in k for item in skill)
                        if(check):
                            # return render_template('check.html',msg =(k,skill) )
                            o = "insert into alloted_resumes values("+str(i[0])+",1,'"+str(i[1])+"');"
                            po = "insert into resumemapping values("+str(i[0])+","+str(id)+",'"+str(ele[1])+"','Sent for Review');"
                            # return render_template('check.html',msg = (po,o))
                            cur.execute(po)
                            cur.execute(o)
                            d = 1
                            f = 1
                        if(d==1):
                            break
                else:
                    for i in datafetched:
                        if(i[0] not in listuser):
                            kf = list(str(i[1]).split(","))
                            k = list(map(lambda x: str(x).lower(), kf))
                            check = any(item in k for item in skill)
                            if(check):
                                # return render_template('check.html',msg = (i[0],listuser))
                                o = "insert into alloted_resumes values("+str(i[0])+",1,'"+str(i[1])+"');"
                                po = "insert into resumemapping values("+str(i[0])+","+str(id)+",'"+str(ele[1])+"','Sent for Review');"
                                # return render_template('check.html',msg =po)
                                cur.execute(po)
                                cur.execute(o)
                                checknumber = 1
                                d = 1
                                f=1
                            if(d==1):
                                break
                    
                    # return render_template('check.html',msg = (i[0],'zsfsda',listuser))       
                    if(checknumber == 0 ):
                        po = 'select * from alloted_resumes order by numberofresumes;'
                        cur.execute(po)
                        gotdata = cur.fetchall()
                        for number in gotdata:
                            kf = list(str(number[2]).split(","))
                            k = list(map(lambda x: str(x).lower(), kf))
                            check = any(item in k for item in skill)
                            if(check):
                                p = number[1]+1
                                o = "update alloted_resumes set numberofresumes=" + str(p) + " where user_id = " +str(number[0])+";"
                                po = "insert into resumemapping values("+str(number[0])+","+str(id)+",'"+str(ele[1])+"','Sent for Review');"
                                # return render_template('check.html',msg =po)
                                cur.execute(po)
                                cur.execute(o)
                                d = 1
                                f=1
                            if(d==1):
                                break
    # return render_template('check.html',msg =fetchData)
    #######################
    #filter the dict with some percentage
    #fetch panelist from the user table for the skill required
    #table - which panelist for which resume
    ########################
    mysql.connection.commit()
    if(f==1):
        flash("Shortlisted Resume have been sent for review"+str(qw)+"")
    else:
        flash("no new resumes for shortlist"+str(qw)+"")
    return redirect(url_for('demand.demander'))