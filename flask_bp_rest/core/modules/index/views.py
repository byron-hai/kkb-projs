# -*- coding: utf-8 -*-
# File: book_api.py
# Date: 11/6/20
# Author: byron

from flask import request, jsonify
from core.modules.index import index_bp
from core.models import Book
from core.utils.status_code import response_code


@index_bp.route('/')
def index():
    books = Book.query.all()
    if books:
        data = {
            'code': '0',
            'msg': 'success',
            'data': [book.to_dict() for book in books]
        }
        return jsonify(data)
    return jsonify({'code': '-1', 'msg': 'No data found'})


