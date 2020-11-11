# -*- coding: utf-8 -*-
# File: status_code.py
# Date: 11/6/20
# Author: byron
class ResponseCode(object):
    @property
    def success(self):
        return {'code': 200, 'msg': 'request success'}

    @staticmethod
    def get_data_success(self, data):
        return {'code': 200, 'msg': 'Get data success', 'data': data}

    @property
    def create_success(self):
        return {'code': 201, 'msg': 'create success'}

    @staticmethod
    def update_success(self, data):
        return {'code': 201, 'msg': 'update success', 'data': data}

    @property
    def register_params_not_fill(self):
        return {'code': 1006, 'msg': 'mobile and password is must for register'}

    @property
    def register_mobile_format_error(self):
        return {'code': 1008, 'msg': 'mobile format error'}

    @property
    def login_info_error(self):
        return {'code': 1001, 'msg': 'username or password error'}

    @property
    def user_not_exist(self):
        return {'code': 1007, 'msg': 'user not existed'}

    @property
    def add_data_fail(self):
        return {'code': 1011, 'msg': 'add data fail'}

    @property
    def update_data_fail(self):
        return {'code': 1012, 'msg': 'update data error'}

    @property
    def delete_data_fail(self):
        return {'code': 1013, 'msg': 'delete data failed'}

    @property
    def get_data_fail(self):
        return {'code': 1014, 'msg': 'Get data failed'}


response_code = ResponseCode()
