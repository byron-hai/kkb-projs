# -*- coding: utf-8 -*-
# @File: __init__.py.py
# @Author: byron
# @Date: 11/11/20

from flask import Blueprint
passport_bp = Blueprint("passport", __name__, url_prefix="/passport")
from . import views
