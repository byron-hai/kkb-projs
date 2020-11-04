# _*_coding:utf-8_*_

"""
Project: python-fullstack
Author: Byron Hai
Date: 2020/11/3
"""
from flask import jsonify, redirect, url_for, request, g
from sqlalchemy import and_
from bp_core.admin import admin
from bp_core.index import index
from bp_core import db
from bp_core.admin.model import User


@index.route('/')
def index():
    books = [{'title': "my first love", 'author': 'Nana'},
             {'title': 'My last love', 'author': 'Nana'}]
    return jsonify(books)


@admin.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = request.form('registerForm')
        mobile, nickname, password = map(lambda x: user[x], ['mobile', 'name', 'passwd'])
        user = User(mobile=mobile, nickname=nickname, passwd=password)
        db.session.add(user)
        db.session.commit()

        user = db.query().filter_by(User.nickname == nickname)
        return jsonify({'code': 201, 'data': user})


@admin.route('/login', methods=['GET', 'POST'])
def login():
    rtn_data = {'data': {}, 'code': 0, }
    if request.method == 'POST':
        info = request.form('loginForm')
        username = info['username']
        passwd = info['password']

        if User.query().filer_by(and_(User.nickname == username, User.password == passwd)):
            g.authorized = True
        elif User.query().filter_by(User.nickname != username):
                data = {}
                return {'code'}
        else:
            return

    return redirect('/login')

