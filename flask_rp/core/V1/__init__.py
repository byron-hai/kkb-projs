# -*- coding: utf-8 -*-
# @File: __init__.py.py
# @Author: byron
# @Date: 11/9/20
from flask import Blueprint
from core.V1 import auth, books, index


def create_blueprint_v1():
    bp_v1 = Blueprint("V1", __name__)
    auth.api.register(bp_v1, url_prefix='/passport')
    books.api.register(bp_v1, url_prefix='/books')
    index.api.register(bp_v1, url_prefix='/index')

    return bp_v1
