# -*- coding: utf-8 -*-
# @File: views.py
# @Author: byron
# @Date: 11/11/20
from flask import request, jsonify, session
from datetime import datetime
import re
from core.modules.passport import passport_bp
from core.models import User, LoginUser
from core import db
from core.utils.status_code import response_code


@passport_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    mobile, nickname, password = map(lambda x: data.get(x), ['mobile', 'username', 'password'])

    if not all([mobile, password]):
        return jsonify(response_code.register_params_not_fill)

    # https://www.cnblogs.com/SuperLee017/p/9544101.html
    if not re.match('1[356789]\d{9}', mobile):
        return jsonify(response_code.register_mobile_format_error)
    user = LoginUser(mobile=mobile, nickname=nickname, password=password)
    user_exist = LoginUser.query.filter_by(mobile=mobile).first()
    if user_exist:
        return jsonify({'code': '-1', 'data': '', 'msg': "user with this name and mobile existed"})

    db.session.add(user)
    err = user.session_commit()

    if not err:
        user = LoginUser.query.filter_by(mobile=mobile, nickname=nickname).first()
        return jsonify({'code': '0', 'data': user.to_dict(), 'msg': 'success'})
    else:
        err_data = {
            'code': '-1',
            'data': err,
            'msg': "commit data to database error"
        }
        return jsonify(err_data)


@passport_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    mobile = data.get('mobile')
    password = data.get('password')

    status = {
        '0': {'code': '0', 'msg': 'success', 'data': None},
        '-1': {'code': '0', 'msg': 'user not active', 'data': ''},
        '-2': {'code': '0', 'msg': 'password error', 'data': ''},
        '-3': {'code': '0', 'msg': 'user not existed', 'data': ''},
    }

    if all([username, password]):
        user = LoginUser.query.filter_by(nickname=username).first()
        if user:
            if user.check_password(password):
                user.last_login = datetime.now()
                session["user_id"] = user.id
                session["mobile"] = user.mobile

                rtn_status = status['0']
                rtn_status['data'] = user.to_dict()
                return jsonify(rtn_status)
            return jsonify(status['-2'])
        return jsonify(status['-3'])

    elif all([mobile, password]):
        user = LoginUser.query.filter_by(mobile=mobile).first()
        if user:
            if user.check_password(password):
                user.last_login = datetime.now()
                session["user_id"] = user.id
                session["mobile"] = user.mobile

                rtn_status = status['0']
                rtn_status['data'] = user.to_dict()
                return jsonify(rtn_status)
            return jsonify(status['-2'])
        return jsonify(status['-3'])
    else:
        return jsonify(response_code.login_info_error)


@passport_bp.route('/logout', methods=['POST'])
def logout():
    """
    logout
    method: POST
    :return: code, msg
    """
    session.pop("user_id", "")
    session.pop("mobile", "")
    return jsonify(response_code.success)
