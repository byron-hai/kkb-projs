# -*- coding: utf-8 -*-
# File: status_code.py
# Date: 11/6/20
# Author: byron

class Response_code(object):
    @property
    def success(self):
        return {'code': 200, 'msg': ''}
