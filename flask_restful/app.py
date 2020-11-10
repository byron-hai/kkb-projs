# -*- coding: utf-8 -*-
# @File: app.py
# @Author: byron
# @Date: 11/10/20

from flask import request, jsonify, redirect, url_for
from flask_restful import Api
from manager import app, db
from core.models import User, Book
from core.utils.status_code import response_code
from core.resources.user_api import UserApi, UsersApi
from core.resources.book_api import BookApi, BooksApi

api = Api(app)

api.add_resource(UsersApi, '/users', '/users/user')
api.add_resource(UserApi, '/users/user/<int:user_id>')
api.add_resource(BooksApi, '/books', '/books/book')
api.add_resource(BookApi, '/books/book/<int:book_id>')


@app.route('/')
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


if __name__ == "__main__":
    app.run()
