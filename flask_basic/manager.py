# _*_coding:utf-8_*_

"""
Project: python-fullstack
Author: Byron Hai
Date: 2020/11/3
"""
from app import app
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


db = SQLAlchemy(app, use_native_unicode='utf8')
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


if __name__ == "__main__":
    manager.run()
