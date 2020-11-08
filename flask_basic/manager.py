# _*_coding:utf-8_*_

"""
Project: python-fullstack
Author: Byron Hai
Date: 2020/11/3
"""
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app_init import app, db
from models import User, Book

manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


if __name__ == "__main__":
    manager.run()
