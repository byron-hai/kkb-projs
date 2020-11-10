# -*- coding: utf-8 -*-
# File: views.py
# Date: 11/6/20
# Author: byron

from flask import request, jsonify
from core.modules.index import index_blu
from core.models import Book
from core.utils.status_code import response_code


@index_blu.route('/')
def index():
    books = Book.query.all()
    if books:
        data = {'books': [book.to_dict() for book in books]}
        return jsonify({'code': '0', 'msg': 'success', 'data': data})
    return jsonify({'code': '-1', 'msg': 'no records found'})


