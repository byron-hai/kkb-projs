# -*- coding: utf-8 -*-
# File: __init__.py.py
# Date: 11/6/20
# Author: byron

from flask import Blueprint

auth_bp = Blueprint('auth', __name__, url_prefix="/passport")
from. import views
