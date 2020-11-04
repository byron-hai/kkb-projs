# _*_coding:utf-8_*_

"""
Project: python-fullstack
Author: Byron Hai
Date: 2020/11/3
"""
from bp_core import db
from datetime import datetime


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category %r>' % self.name


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(20))
    price = db.Column(db.Float)
    status = db.Column(db.Enums([0, 1]))
    create_date = db.Column(db.String(20), default=datetime.now)
    update_date = db.Column(db.String(20), default=datetime.now, onupdate=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('books', lazy='dynamic'))

    def __init__(self, name, category, price, user_id, status):
        self.name = name
        self.category = category
        self.price = price
        self.user_id = user_id
        self.status = status

    def __repr__(self):
        return '<Book %r>' % self.name
