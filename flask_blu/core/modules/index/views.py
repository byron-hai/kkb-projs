# -*- coding: utf-8 -*-
# File: views.py
# Date: 11/6/20
# Author: byron

from flask import request, jsonify
from core.modules.index import index_blu
from core.models import Book, Category
from core.utils.status_code import response_code


@index_blu.route('/')
def index():
    books = Book.query.all()
    categories = Category.query.all()

    if books:
        books = [book.to_dict() for book in books]
        categories = [cate.to_dict() for cate in categories]
        data = {'categories': categories, 'books': books}
        return jsonify(response_code.get_data_success(data))

    return jsonify(response_code.success)

