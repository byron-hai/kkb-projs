# _*_coding:utf-8_*_

"""
Project: python-fullstack
Author: Byron Hai
Date: 2020/11/3
"""
from flask import Blueprint
admin = Blueprint('admin', __name__, url_prefix='/admin')
