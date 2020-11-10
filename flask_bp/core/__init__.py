# -*- coding: utf-8 -*-
# File: __init__.py.py
# Date: 11/6/20
# Author: byron

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from core.utils.converter import RegexConverter
from config.config import Config, configs

db = SQLAlchemy()


def create_app(config_name):
    config = configs[config_name]
    app = Flask(__name__)
    app.config.from_object(config)
    app.url_map.converters['re'] = RegexConverter
    db.init_app(app)

    from core.modules.auth import auth_blu
    app.register_blueprint(auth_blu)

    from core.modules.index import index_blu
    app.register_blueprint(index_blu)

    from core.modules.book import book_blu
    app.register_blueprint(book_blu)

    return app
