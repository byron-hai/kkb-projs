# -*- coding: utf-8 -*-
# File: __init__.py.py
# Date: 11/6/20
# Author: byron

from app_init import app, db
from flask import request, jsonify
from utils.status_code import response_code
from utils.common import login_check
from models import User, Book


@app.route('/passport/register', methods=['POST'])
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


@app.route('/passport/login', methods=['POST'])
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
        return jsonify()


@app.route('/')
def index():
    books = Book.query.all()
    if books:
        data = {'books': [book.to_dict() for book in books]}
        return jsonify({'code': '0', 'msg': 'success', 'data': data})
    return jsonify({'code': '-1', 'msg': 'no records found'})


@app.route('/users')
# @login_check
def get_users():
    users = User.query.all()
    if users:
        users = [user.to_dict() for user in users]
        return jsonify({'code': '0', 'msg': 'success', 'data': users})
    return jsonify({'code': '-1', 'msg': 'No records found', 'data': ''})


# Books
# Select
@app.route('/books')
def get_books():
    books = Book.query.all()
    if books:
        books = [book.to_dict() for book in books]
        return jsonify({'code': '0', 'msg': 'success', 'data': books})

    return jsonify(code='-1', msg="No records found")


@app.route('/books/book/<int:book_id>')
def get_book(book_id):
    book = Book.query.get(book_id)
    if book:
        return jsonify({'code': '0', 'message': 'success', 'data': book.to_dict()})
    return jsonify({'code': '-1', 'msg': 'No records found'})


@app.route('/books/book', methods=['POST'])
# @login_check
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
@app.route('/books/book/<int:book_id>', methods=['PATCH'])
# @login_check
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
        book.session_commit()

        book = Book.query.get(book_id)
        if book:
            return jsonify({'code': '0', 'msg': 'success', 'data': book.to_dict()})
        return jsonify({'code': '-1', 'msg': 'update book info failed'})
    return jsonify(response_code.get_data_fail)


# Delete
@app.route('/books/book/<int:book_id>', methods=['DELETE'])
# @login_check
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


if __name__ == "__main__":
    app.run()
