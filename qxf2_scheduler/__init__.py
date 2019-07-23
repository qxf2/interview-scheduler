from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import qxf2_scheduler.db_config as conf 

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://%s:%s@%s/%s'%(conf.USERNAME,conf.PASSWORD,conf.SERVER,conf.DATABASE)
#db = SQLAlchemy(app)

from qxf2_scheduler import routes