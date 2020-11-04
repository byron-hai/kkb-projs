# _*_coding:utf-8_*_

"""
Project: python-fullstack
Author: Byron Hai
Date: 2020/11/3
"""
from flask import Blueprint
books = Blueprint('books', __name__, url_prefix='/books')
