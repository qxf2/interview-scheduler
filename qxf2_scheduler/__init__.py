from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
import qxf2_scheduler.db_config as conf
import qxf2_scheduler.email_config as email_conf
import os

app = Flask(__name__)
db_file = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'data/interviewscheduler.db'))
app.secret_key = "qxf2-database"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///%s"%db_file
db = SQLAlchemy(app)

app.config.update(
	DEBUG=True,
	#EMAIL SETTINGS
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USERNAME = email_conf.MAIL_USERNAME,
	MAIL_PASSWORD = email_conf.MAIL_PASSWORD
	)


from qxf2_scheduler import routes
from qxf2_scheduler import candidates
from qxf2_scheduler import rounds
from qxf2_scheduler import status
