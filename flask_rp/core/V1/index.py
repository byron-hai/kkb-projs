# -*- coding: utf-8 -*-
# File: auth.py
# Date: 11/6/20
# Author: byron

from flask import jsonify
from core.utils.red_print import RedPrint
from core.models import Book

api = RedPrint("index")


@api.route('/')
def index():
    books = Book.query.all()
    if books:
        data = {'books': [book.to_dict() for book in books]}
        return jsonify({'code': '0', 'msg': 'success', 'data': data})
    return jsonify({'code': '-1', 'msg': 'no records found'})
