# -*- coding: utf-8 -*-
# File: __init__.py.py
# Date: 11/6/20
# Author: byron

from flask import Flask, request, g, current_app, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_session import Session
from core.utils.converter import RegexConverter, MobileConverter
from config.config import Config, configs
from redis import StrictRedis
from core.utils import constants

db = SQLAlchemy()
redis_store = None


def create_app(config_name):
    config = configs[config_name]
    app = Flask(__name__)
    app.config.from_object(config)
    app.url_map.converters['re'] = RegexConverter
    app.url_map.converters['mobile'] = MobileConverter
    db.init_app(app)

    global redis_store
    redis_store = StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT,
                              decode_responses=True)  # create redis object

    Session(app)
    jwt = JWTManager(app)

    @app.before_request
    def before_request():
        token = request.headers.get('token')
        user_id = redis_store.get("token:%s" % token)

        if user_id:
            from core.models import LoginUser
            g.current_user = LoginUser.query.get(user_id)
            g.token = token
            count = 0

            try:
                count = redis_store.get("request_count:%s" % user_id) or 0
            except Exception as e:
                current_app.logger.error(e)

            if isinstance(count, str):
                count = int(count)

            count += 1
            try:
                redis_store.set("request_count:%s" % user_id, count,
                                constants.REQUEST_COUNT_REDIS_EXPIRES)
            except Exception as e:
                current_app.logger.error(e)
        return

    # Register blueprints
    from core.modules.auth import auth_bp
    app.register_blueprint(auth_bp)

    from core.modules.passport import passport_bp
    app.register_blueprint(passport_bp)

    from core.modules.index import index_bp
    app.register_blueprint(index_bp)

    from core.modules.book import book_bp
    app.register_blueprint(book_bp)

    return app
