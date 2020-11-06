# -*- coding: utf-8 -*-
# File: model.py
# Date: 11/4/20
# Author: byron
from manager import db
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError


class BaseModel(object):
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def add(self, obj):
        db.session.add(obj)
        session_commit()

    @staticmethod
    def update(self):
        return session_commit()

    def delete(self, id):
        self.query.filter_by(id=id).delete()
        return session_commit()


class User(BaseModel, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mobile = db.Column(db.String(20), unique=True)
    nickname = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(20), nullable=False)
    last_login = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, mobile, nickname, passwd):
        self.mobile = mobile
        self.nickname = nickname
        self.password = passwd

    # def __repr__(self):
    #     return "<User %r>" % self.nickname
    def check_password(self, password):
        return True if password == self.password else False

    def to_dict(self):
        res_dict = {
            'id': self.id,
            'mobile': self.mobile,
            'last_login': self.last_login
        }
        return res_dict

    # @staticmethod
    # def add(self, user):
    #     db.session.add(user)
    #     session_commit()
    #
    # @staticmethod
    # def update(self):
    #     return session_commit()
    #
    # def delete(self, id):
    #     self.query.filter_by(id=id).delete()
    #     return session_commit()


class Category(BaseModel, db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name

    def to_dict(self):
        return {'id': self.id, 'name': self.name}


class Book(BaseModel, db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.Integer)
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
        return session_commit()


def session_commit():
    try:
        db.session.commit()
    except SQLAlchemyError as err:
        db.session.rollback()
        return str(err)
