# _*_coding:utf-8_*_

"""
Project: python-fullstack
Author: Byron Hai
Date: 2020/11/3
"""
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from api_app import create_app, db

app = create_app("development")
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


if __name__ == "__main__":
    manager.run()
