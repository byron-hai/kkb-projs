# -*- coding: utf-8 -*-
# @File: __init__.py.py
# @Author: byron
# @Date: 11/7/20
from flask import Blueprint
from flask_restful import Api
from .user_api import UserApi, UsersApi

user_bp = Blueprint("users", __name__)
api = Api(user_bp)
api.add_resource(UsersApi, '/users', '/users/user')
api.add_resource(UserApi, '/users/user/<int:user_id>')
