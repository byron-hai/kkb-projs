# -*- coding: utf-8 -*-
# File: __init__.py.py
# Date: 11/6/20
# Author: byron


from flask import Flask, request, redirect, jsonify, url_for
from utils.converter import RegexConverter
from config.config import Config
from utils.status_code import response_code


app = Flask(__name__)
app.config.from_object(Config)
app.url_map.converters['re'] = RegexConverter

from model import User, Book, Category


@app.route('/register', methods=['POST'])
def register():
    data = request.json
    mobile, nickname, password = map(lambda x: data.get(x), ['mobile', 'username', 'password'])
    user = User(mobile=mobile, nickname=nickname, passwd=password)
    err = user.add(user)

    if not err:
        return jsonify(response_code.success)
    else:
        response_code.user_not_exist['sql_err'] = err
        return jsonify(response_code.user_not_exist)


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    mobile = data.get('mobile')
    password = data.get('password')

    if all([username, password]):
        user = User.query.get(nickname=username)
        if user:
            if user.check_password(password):
                data = {'code': 200,
                        'data': user.to_dict()}
                return jsonify(data)
            return jsonify(response_code.login_info_error)
        return jsonify(response_code.user_not_exist)

    elif all([mobile, password]):
        user = User.query.get(mobile=mobile)
        if user:
            if user.check_password(password):
                data = {'code': 200,
                        'data': user.to_dict()}
                return jsonify(data)
            return jsonify(response_code.login_info_error)
        return jsonify(response_code.user_not_exist)
    else:
        return jsonify(response_code.login_info_error)


@app.route('/')
def index():
    books = Book.query.all()
    categories = Category.query.all()

    data = {'books': [book.to_dict() for book in books],
            'categories': [cate.to_dict() for cate in categories]}
    return jsonify(data)


@app.route('/users')
def get_users():
    users = User.query.all()
    if users:
        users = [user.to_dict() for user in users]
        return jsonify(response_code.get_data_success(users))
    return jsonify(response_code.get_data_fail)


# Books
# Select
@app.route('/books')
def get_books():
    books = Book.query.all()
    if books:
        books = [book.to_dict() for book in books]
        return jsonify(response_code.get_data_success(books))

    return jsonify(response_code.get_data_fail)


@app.route('/books/<book_id>', methods=['POST'])
def get_book(book_id):
    book = Book.query.get(id=book_id)
    if book:
        return jsonify(response_code.get_data_success([book.to_dict()]))
    return jsonify(response_code.get_data_fail)


@app.route('/books/add', methods=['POST'])
def add():
    data = request.json
    name = data.get('name')
    category = data.get('category')
    price = data.get('price')
    # user_id = ""
    user_id = ""
    book = Book(name, category, price, user_id)
    book.add(book)

    return redirect(url_for('index'))


@app.route('/books/<book_id>')
def book_info(book_id):
    book = Book.query.get(id=book_id)
    return jsonify(book)


# Update
@app.route('/books/<book_id>/update', methods=['POST'])
def update(book_id):
    pass


# Delete
@app.route('/<book_id>/delete', methods=['POST'])
def delete(book_id):
    book = Book.query.get(id=book_id)
    if book:
        book.delete()


if __name__ == "__main__":
    app.run()
