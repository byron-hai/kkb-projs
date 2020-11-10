# -*- coding: utf-8 -*-
# File: models.py
# Date: 11/4/20
# Author: byron
from api_app import db
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError


class BaseModel(object):
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    @staticmethod
    def session_commit():
        try:
            db.session.commit()
        except SQLAlchemyError as err:
            db.session.rollback()
            return str(err)


class User(BaseModel, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mobile = db.Column(db.String(20), unique=True)
    nickname = db.Column(db.String(50), unique=True)
    _password = db.Column(db.String(20), nullable=False)
    last_login = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, mobile, nickname, passwd):
        self.mobile = mobile
        self.nickname = nickname
        self._password = passwd

    def __repr__(self):
        return "<User %r>" % self.nickname

    def check_password(self, password):
        return True if password == self._password else False

    def to_dict(self):
        res_dict = {
            'id': self.id,
            'nickname': self.nickname,
            'mobile': self.mobile,
            'last_login': self.last_login
        }
        return res_dict


class Book(BaseModel, db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50))
    price = db.Column(db.Float)
    user_id = db.Column(db.Integer)
    status = db.Column(db.Enum('0', '1'), default='0')

    def __init__(self, name, category, price, user_id):
        self.name = name
        self.category = category
        self.price = price
        self.user_id = user_id

    def __repr__(self):
        return "<Book %r>" % self.name

    def to_dict(self):
        res_dict = {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'price': self.price,
            'user_id': self.user_id,
            'status': self.status
        }
        return res_dict

    def delete(self):
        self.status = "1"
        return self.session_commit()

