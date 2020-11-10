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

    from core.modules.auth import auth_bp
    app.register_blueprint(auth_bp)

    from core.modules.index import index_bp
    app.register_blueprint(index_bp)

    from core.modules.books import book_bp
    app.register_blueprint(book_bp)

    from core.modules.users import user_bp
    app.register_blueprint(user_bp)

    return app
