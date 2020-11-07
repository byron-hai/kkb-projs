# -*- coding: utf-8 -*-
# @File: __init__.py.py
# @Author: byron
# @Date: 11/5/20

from flask import Blueprint
book_blu = Blueprint('books', __name__, url_prefix='/books')
from . import views
