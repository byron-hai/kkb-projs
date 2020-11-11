# -*- coding: utf-8 -*-
# @File: views.py
# @Author: byron
# @Date: 11/11/20
import hashlib
import re
import time
from flask import request, jsonify, current_app, g
from datetime import datetime
from core.modules.token_passport import token_passport_bp
from core.models import LoginUser
from core import db, redis_store
from core.utils.status_code import response_code
from core.utils import constants


@token_passport_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    mobile, nickname, password = map(lambda x: data.get(x), ['mobile', 'username', 'password'])

    if not all([mobile, password]):
        return jsonify(response_code.register_params_not_fill)

    # https://www.cnblogs.com/SuperLee017/p/9544101.html
    if not re.match('1[356789]\\d{9}', mobile):
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


@token_passport_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    mobile = data.get('mobile')
    password = data.get('password')

    if all([username, password]):
        try:
            user = LoginUser.query.filter_by(nickname=username).first()
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(response_code.get_data_fail)

        if not user:
            return jsonify(response_code.user_not_exist)

        if not user.check_password(password):
            return jsonify(response_code.login_info_error)

    elif all([mobile, password]):
        try:
            user = LoginUser.query.filter_by(mobile=mobile).first()
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(response_code.user_not_exist)

        if not user:
            return jsonify(response_code.user_not_exist)

        if not user.check_password(password):
            return jsonify(response_code.login_info_error)

        # Generate token
        m = hashlib.md5()
        m.update(mobile.encode("utf-8"))
        m.update(password.encode("utf-8"))
        m.update(str(int(time.time())).encode("utf-8"))
        token = m.hexdigest()

        user_id = user.id
        user_data = {
            "user_id": user_id,
            "mobile": user.mobile,
            "token": token
        }

        try:
            pipeline = redis_store.pipeline()
            pipeline.hmset("user:%s" % user_id, user_data)
            pipeline.set("token:%s" % token, user_id)
            pipeline.expire("token:%s" % token, constants.LOGIN_INFO_REDIS_EXPIRES)
            pipeline.execute()
        except Exception as e:
            current_app.logger.error(e)

        user.last_login = datetime.now()
        user.session_commit()
        response_dict = response_code.success
        response_dict['token'] = token
        return jsonify(response_dict)


@token_passport_bp.route('/logout', methods=['POST'])
def logout():
    """
    logout
    method: POST
    :return: code, msg
    """
    user_id = g.current_user.id
    token = g.token
    try:
        redis_store.delete("user:%s" % user_id)
        redis_store.delete("token:%s" % token)
    except Exception as e:
        current_app.logger.error(e)

    return jsonify(response_code.success)

