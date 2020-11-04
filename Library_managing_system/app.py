# _*_coding:utf-8_*_

"""
Project: python-fullstack
Author: Byron Hai
Date: 2020/11/3
"""
from flask import Flask, redirect, url_for, jsonify
from flask_script import Manager
from config.config import Config
from flask_sqlalchemy import SQLAlchemy
from common.converter import RegexConverter


app = Flask(__name__)
app.config.from_object(Config)
app.url_map.converters['re'] = RegexConverter
db = SQLAlchemy(app)
manager = Manager(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column()

@app.route('/')
def home():
    book_data = []
    return jsonify(book_data)

@app.route('/login')
def login():
    return redirect(url_for('home'))