# -*- coding: utf-8 -*-
# File: views.py
# Date: 11/6/20
# Author: byron

from flask import request, jsonify
from core.modules.index import index_bp
from core.models import Book, LoginUser
from core.utils.common import login_session_check, login_token_check
from core.utils.status_code import response_code


@index_bp.route('/')
def index():
    books = Book.query.all()
    if books:
        data = {'books': [book.to_dict() for book in books]}
        return jsonify({'code': '0', 'msg': 'success', 'data': data})
    return jsonify({'code': '-1', 'msg': 'no records found'})


@index_bp.route('/users')
@login_session_check
def get_users():
    users = LoginUser.query.all()
    if not users:
        return jsonify({'code': -1, 'msg': 'get user info failed'})

    data = {'code': 0,
            'msg': 'success',
            'data': [user.to_dict() for user in users]}

    return jsonify(data)

