from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail, Message
from flaskext.markdown import Markdown
import qxf2_scheduler.db_config as conf
import qxf2_scheduler.email_config as email_conf
from flask_seeder import FlaskSeeder
import os
import logging

app = Flask(__name__)
db_file = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'data/interviewscheduler.db'))
app.secret_key = "qxf2-database"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///%s"%db_file
logging.basicConfig(filename='record.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
db = SQLAlchemy(app)
Markdown(app)
db.init_app(app)
seeder = FlaskSeeder()
seeder.init_app(app,db)


app.config.update(
	DEBUG=True,
	#EMAIL SETTINGS
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USE_TLS = False,
	MAIL_USERNAME = email_conf.MAIL_USERNAME,
	MAIL_PASSWORD = email_conf.MAIL_PASSWORD,
	MAIL_DEFAULT_SENDER = email_conf.MAIL_USERNAME
	)


login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)



from qxf2_scheduler import routes
from qxf2_scheduler import candidates
from qxf2_scheduler import rounds
from qxf2_scheduler import status
from qxf2_scheduler import reset_password