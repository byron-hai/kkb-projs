# -*- coding: utf-8 -*-
# File: __init__.py.py
# Date: 11/6/20
# Author: byron

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_session import Session
from core.utils.converter import RegexConverter
from config.config import Config, configs
from redis import StrictRedis

db = SQLAlchemy()


def create_app(config_name):
    config = configs[config_name]
    app = Flask(__name__)
    app.config.from_object(config)
    app.url_map.converters['re'] = RegexConverter
    db.init_app(app)

    global redis_store
    redis_store = StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT,
                              decode_responses=True)  # create redis object

    Session(app)
    jwt = JWTManager(app)

    from core.modules.auth import auth_bp
    app.register_blueprint(auth_bp)

    from core.modules.passport import passport_bp
    app.register_blueprint(passport_bp)

    from core.modules.index import index_bp
    app.register_blueprint(index_bp)

    from core.modules.book import book_bp
    app.register_blueprint(book_bp)

    return app
