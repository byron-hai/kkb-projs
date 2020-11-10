# -*- coding: utf-8 -*-
# File: auth.py
# Date: 11/6/20
# Author: byron

from flask import request, jsonify
from core.utils.red_print import RedPrint
from core.models import User
from core import db
from core.utils.status_code import response_code

api = RedPrint("auth")


@api.route('/register', methods=['POST'])
def register():
    data = request.json
    mobile, nickname, password = map(lambda x: data.get(x), ['mobile', 'username', 'password'])
    user = User(mobile=mobile, nickname=nickname, passwd=password)
    user_exist = User.query.filter_by(mobile=mobile).first()
    if user_exist:
        return jsonify({'code': '-1', 'data': '', 'msg': "user with this name and mobile existed"})

    db.session.add(user)
    err = user.session_commit()

    if not err:
        user = User.query.filter_by(mobile=mobile, nickname=nickname).first()
        return jsonify({'code': '0', 'data': user.to_dict(), 'msg': 'success'})
    else:
        err_data = {
            'code': '-1',
            'data': err,
            'msg': "commit data to database error"
        }
        return jsonify(err_data)


@api.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    mobile = data.get('mobile')
    password = data.get('password')

    status = {
        '0': {'code': '0', 'msg': 'success', 'data': None},
        '-1': {'code': '0', 'msg': 'user not active', 'data': ''},
        '-2': {'code': '0', 'msg': 'password error', 'data': ''},
        '-3': {'code': '0', 'msg': 'user not existed', 'data': ''}
    }

    if all([username, password]):
        user = User.query.filter_by(nickname=username).first()
        if user:
            if user.check_password(password):
                rtn_status = status['0']
                rtn_status['data'] = user.to_dict()
                return jsonify(rtn_status)
            return jsonify(status['-2'])
        return jsonify(status['-3'])

    elif all([mobile, password]):
        user = User.query.filter_by(mobile=mobile).first()
        if user:
            if user.check_password(password):
                rtn_status = status['0']
                rtn_status['data'] = user.to_dict()
                return jsonify(rtn_status)
            return jsonify(status['-2'])
        return jsonify(status['-3'])
    else:
        return jsonify(response_code.login_info_error)
