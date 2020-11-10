# -*- coding: utf-8 -*-
# File: __init__.py.py
# Date: 11/6/20
# Author: byron

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from core.utils.converter import RegexConverter
from config.config import configs

db = SQLAlchemy()


def create_app(config_name):
    config = configs[config_name]
    app = Flask(__name__)
    app.config.from_object(config)
    app.url_map.converters['re'] = RegexConverter
    db.init_app(app)

    from core.V1 import create_blueprint_v1
    app.register_blueprint(create_blueprint_v1(), url_prefix='/v1')

    return app
