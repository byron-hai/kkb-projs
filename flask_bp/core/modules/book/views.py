# -*- coding: utf-8 -*-
# @File: views.py
# @Author: byron
# @Date: 11/5/20
from flask import request, redirect, jsonify
from core.modules.book import book_bp
from core.models import Book
from core import db
from core.utils.common import login_session_check, login_token_check
from core.utils.status_code import response_code


@book_bp.route('/')
def get_books():
    books = Book.query.all()
    if books:
        books = [book.to_dict() for book in books]
        return jsonify({'code': '0', 'msg': 'success', 'data': books})

    return jsonify(code='-1', msg="No records found")


@book_bp.route('/book/<int:book_id>')
def get_book(book_id):
    book = Book.query.get(book_id)
    if book:
        return jsonify({'code': '0', 'message': 'success', 'data': book.to_dict()})
    return jsonify({'code': '-1', 'msg': 'No records found'})


@book_bp.route('/book', methods=['POST'])
@login_session_check
def add():
    data = request.json
    name = data.get('name')
    category = data.get('category')
    price = data.get('price')
    user_id = 1  # Todo: Get user_id from cookie

    is_exist = Book.query.filter_by(name=name).first()
    if is_exist:
        jsonify({'code': '-1', 'msg': "Add book failed", 'error': "book with this name existed"})

    book = Book(name, category, price, user_id)
    db.session.add(book)
    err = book.session_commit()

    if not err:
        book = Book.query.filter_by(name=name).first()
        return jsonify({'code': '0', 'data': book.to_dict(), 'msg': 'success'})
    return jsonify({'code': '-1', 'msg': 'add book failed', 'error': err})


# Update
@book_bp.route('/book/<int:book_id>', methods=['PATCH'])
@login_session_check
def update(book_id):
    data = request.json
    name = data.get('name')
    category = data.get('category')
    price = data.get('price')

    book = Book.query.get(book_id)
    if book:
        if name:
            book.name = name
        if category:
            book.category = category
        if price:
            book.price = price
        err = book.session_commit()

        if not err:
            book = Book.query.get(book_id)
            return jsonify({'code': '0', 'msg': 'success', 'data': book.to_dict()})
        return jsonify({'code': '-1', 'msg': 'update book info failed', 'error': err})
    return jsonify({'code': '-1', 'msg': 'get book failed'})


# Delete
@book_bp.route('/book/<book_id>', methods=['DELETE'])
@login_session_check
def delete(book_id):
    book = Book.query.get(book_id)
    if book:
        book.status = '1'
        err = book.session_commit()

        if not err:
            book = Book.query.get(book_id)
            return jsonify({'code': '0', 'msg': 'success', 'data': book.to_dict()})
        return jsonify({'code': '-1', 'msg': 'delete failed'})
    return jsonify({'code': '-1', 'msg': 'book not found'})
