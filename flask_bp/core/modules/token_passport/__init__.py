# -*- coding: utf-8 -*-
# @File: __init__.py.py
# @Author: byron
# @Date: 11/11/20
from flask import Blueprint
token_passport_bp = Blueprint("token_passport", __name__, "/token_passport")
from . import views
