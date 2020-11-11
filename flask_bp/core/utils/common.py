# -*- coding: utf-8 -*-
# @File: common.py
# @Author: byron
# @Date: 11/7/20

from functools import wraps
from flask import session, current_app, g, jsonify, request
from core.utils.status_code import response_code
from core import redis_store


def login_session_check(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user_id = session.get("user_id")

        user = None
        if user_id:
            try:
                from core.models import LoginUser
                user = LoginUser.query.get(user_id)
            except Exception as err:
                current_app.logger.error(err)
        g.user = user

        if not user:
            return jsonify(response_code.user_not_exist)
        return func(*args, **kwargs)
    return wrapper


def login_token_check(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.header.get("token")
        if not token:
            return jsonify(response_code.user_not_exist)

        user_id = redis_store.get('token:%s' % token)
        if not user_id or token != redis_store.hget("user:%s" % user_id, 'token'):
            return jsonify(response_code.check_data_error)

        return func(*args, **kwargs)
    return wrapper
