# -*- coding: utf-8 -*-
# File: __init__.py.py
# Date: 11/6/20
# Author: byron


from flask import Flask, request, redirect, jsonify, url_for
from sqlalchemy import and_

from utils.converter import RegexConverter
from config.config import Config
from utils.status_code import Response_code


app = Flask(__name__)
app.config.from_object(Config)
app.url_map.converters['re'] = RegexConverter

from model import User, Book, Category


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = request.form('registerForm')
        mobile, nickname, password = map(lambda x: user[x], ['mobile', 'name', 'passwd'])
        user = User(mobile=mobile, nickname=nickname, passwd=password)
        err = user.add(user)

        if not err:
            return jsonify(Response_code.success)
        else:
            Response_code.user_not_exist['sql_err'] = err
            return jsonify(Response_code.user_not_exist)


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        info = request.form('loginForm')
        username = info['username']
        passwd = info['password']

        if User.query.filer_by(and_(User.nickname == username, User.password == passwd)).first():
            pass
        elif User.query.filter_by(User.nickname != username).first():
            return {'code'}
        else:
            return


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
    data = {
        'code': 1,
        'msg': '用户信息获取成功',
        'data': [user.to_dict() for user in users],
    }
    return jsonify(data)


# Books
# Select
@app.route('/books')
def get_books():
    books = Book.query.all()
    categories = Category.query.all()

    data = {'books': [book.to_dict() for book in books],
            'categories': [cate.to_dict() for cate in categories]}

    return jsonify(data)


@app.route('/books/<book_id>', methods=['POST'])
def get_book(book_id):
    book = Book.query.get(id=book_id)
    if book:
        pass

    else:
        pass


@app.route('/books/add', methods=['POST'])
def add():
    data = request.json()
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
