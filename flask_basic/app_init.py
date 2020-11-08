# -*- coding: utf-8 -*-
# File: __init__.py.py
# Date: 11/6/20
# Author: byron


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from utils.converter import RegexConverter
from config.config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.url_map.converters['re'] = RegexConverter
db = SQLAlchemy(app)

