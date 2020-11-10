# -*- coding: utf-8 -*-
# File: __init__.py.py
# Date: 11/6/20
# Author: byron

from flask import Blueprint
index_bp = Blueprint('index', __name__, url_prefix='/index')
from . import views
