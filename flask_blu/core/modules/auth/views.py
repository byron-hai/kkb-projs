# -*- coding: utf-8 -*-
# File: views.py
# Date: 11/6/20
# Author: byron
from flask import request, jsonify
from core.modules.auth import auth_blu
from core.models import User
from core.utils.status_code import response_code


@auth_blu.route('/register', methods=['POST'])
def register():
    data = request.json
    mobile, nickname, password = map(lambda x: data.get(x), ['mobile', 'username', 'password'])
    user = User(mobile=mobile, nickname=nickname, passwd=password)
    err = user.add(user)

    if not err:
        return jsonify(response_code.success)
    else:
        response_code.user_not_exist['sql_err'] = err
        return jsonify(response_code.user_not_exist)


@auth_blu.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    mobile = data.get('mobile')
    password = data.get('password')

    if all([username, password]):
        user = User.query.get(nickname=username)
        if user:
            if user.check_password(password):
                data = {'code': 200,
                        'data': user.to_dict()}
                return jsonify(data)
            return jsonify(response_code.login_info_error)
        return jsonify(response_code.user_not_exist)

    elif all([mobile, password]):
        user = User.query.get(mobile=mobile)
        if user:
            if user.check_password(password):
                data = {'code': 200,
                        'data': user.to_dict()}
                return jsonify(data)
            return jsonify(response_code.login_info_error)
        return jsonify(response_code.user_not_exist)
    else:
        return jsonify(response_code.login_info_error)
