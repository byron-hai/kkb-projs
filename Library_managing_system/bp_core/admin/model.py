# _*_coding:utf-8_*_

"""
Project: python-fullstack
Author: Byron Hai
Date: 2020/11/3
"""
from bp_core.admin import admin
from bp_core import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mobile = db.Column(db.String(20), unique=True)
    nickname = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(20), nullable=False)

    def __init__(self, mobile, nickname, passwd):
        self.mobile = mobile
        self.nickname = nickname
        self.password = passwd

    def __repr__(self):
        return self.nickname
