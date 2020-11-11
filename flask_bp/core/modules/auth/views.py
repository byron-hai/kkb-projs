# -*- coding: utf-8 -*-
# File: views.py
# Date: 11/6/20
# Author: byron
from flask import request, jsonify
from core.modules.auth import auth_bp
from core.models import User
from core import db
from core.utils.common import login_check
from core.utils.status_code import response_code


@auth_bp.route("/users")
def get_users():
    users = User.query.all()
    if users:
        data = {
            "code": '0',
            "msg": 'success',
            "data": [user.to_dict() for user in users]
        }

        return jsonify(data)
    return jsonify({'code': '-1', 'msg': "No data found"})
