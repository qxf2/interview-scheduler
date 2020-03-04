from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from qxf2_scheduler import models
from qxf2_scheduler import db
from qxf2_scheduler.__init__ import app
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand

migrate=Migrate(app, db)
manager=Manager(app)


if __name__ == "__main__":
    manager.run()