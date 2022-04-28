from flask import Flask
from sysconfig import os
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
db = SQLAlchemy(app)
Migrate(app,db)



######################################









from projectfolder.errorpages.handlers import error_pages
from projectfolder.demand.views import demand
from projectfolder.resume.views import resume
app.register_blueprint(error_pages)
app.register_blueprint(demand)
app.register_blueprint(resume)