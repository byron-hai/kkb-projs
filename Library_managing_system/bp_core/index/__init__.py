# _*_coding:utf-8_*_

"""
Project: python-fullstack
Author: Byron Hai
Date: 2020/11/3
"""
from flask import Blueprint
index = Blueprint('index', __name__)
from . import views

