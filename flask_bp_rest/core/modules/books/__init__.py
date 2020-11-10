# -*- coding: utf-8 -*-
# @File: __init__.py.py
# @Author: byron
# @Date: 11/5/20

from flask import Blueprint
from flask_restful import Api
from .book_api import BooksApi, BookApi

book_bp = Blueprint('books', __name__)
api = Api(book_bp)
api.add_resource(BooksApi, '/books', '/books/book')
api.add_resource(BookApi, '/books/book/<int:book_id>')
