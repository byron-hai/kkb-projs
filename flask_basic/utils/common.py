# -*- coding: utf-8 -*-
# @File: common.py
# @Author: byron
# @Date: 11/7/20

from functools import wraps
from flask import session, current_app, g, jsonify, request
from utils.status_code import response_code


def login_check(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user_id = session.get("user_id")

        user = None
        if user_id:
            try:
                from models import User
                user = User.query.get(user_id)
            except Exception as err:
                current_app.logger.error(err)
        g.user = user

        if not user:
            return jsonify(response_code.user_not_exist)
        return func(*args, **kwargs)
    return wrapper
