# _*_coding:utf-8_*_

"""
Project: python-fullstack
Author: Byron Hai
Date: 2020/11/2
"""
from flask import Flask
from sqlalchemy import SQLAlchemy
app = Flask(__name__)
db = SQLAlchemy(app)

from bp_core.admin import admin
app.register_blueprint(admin)

from bp_core.index import index
app.register_blueprint(index)

from bp_core.books import books
app.register_blueprint(books)
