from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import qxf2_scheduler.db_config as conf
import os

app = Flask(__name__)
db_file = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'data/interviewscheduler.db'))
app.secret_key = "qxf2-database"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///%s"%db_file
db = SQLAlchemy(app)

from qxf2_scheduler import routes
from qxf2_scheduler import candidates
