from flask import Flask
from sysconfig import os
from flask_mail import Mail, Message
import os
import smtplib, ssl
from flask_mysqldb import MySQL
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)





###################################
##### DATABASE ####################

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' +os.path.join(basedir,'data.sqlite')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =False
app.config['SECRET_KEY'] = "sree is the key"
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'sree9078'
app.config['MYSQL_DB'] = 'project'
db = SQLAlchemy(app)
Migrate(app,db)

mysql = MySQL(app)
##########################################################
# mail_settings = {
#     "MAIL_SERVER": 'smtp.office365.com',
#     "MAIL_PORT": 587,
#     "MAIL_USE_TLS": True,
#     "MAIL_USE_SSL": False,
#     "MAIL_USERNAME": os.environ['newsreenivastry'],
#     "MAIL_PASSWORD": os.environ['systemrequest@123']
# }

# port = 465  # For starttls
# smtp_server = "smtp.office365.com"
# sender_email = "newsreenivastry@outlook.com"
# receiver_email = "sreenivasmsa@gmail.com"
# password = 'systemrequest@123'
# message = "This is the mail saying new job demand has been updated"
# context = ssl.create_default_context()
# with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
#     server.login(sender_email, password)
#     # server.sendmail(sender_email, receiver_email, message)
###########################################################
# def move_forward():
#     with app.app_context():
#         cur = mysql.connection.cursor()
#     cur.execute("select * from session_table order by entry desc limit 1;")
#     data = cur.fetchone()
#     if(data[4] != 'N'):
#         session_info['loggedin'] = True
#         session_info['id'] = data[1]
#         session_info['username'] = data[2]
#     else:
#         session_info = {}

#move_forward()
###############################################

from projectfolder.errorpages.handlers import error_pages
from projectfolder.demand.views import demand
from projectfolder.resume.views import resume
from projectfolder.core.views import core
from projectfolder.triage.views import triage
from projectfolder.settings.views import settings
app.register_blueprint(error_pages)
app.register_blueprint(core)
app.register_blueprint(demand)
app.register_blueprint(settings)
app.register_blueprint(resume)
app.register_blueprint(triage)