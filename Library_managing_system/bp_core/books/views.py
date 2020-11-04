# _*_coding:utf-8_*_

"""
Project: python-fullstack
Author: Byron Hai
Date: 2020/11/3
"""
from flask import request, redirect, url_for, jsonify, abort
from bp_core import db
from bp_core.books import books
from .model import Books


# Add
@books.route('/add', methods=['POST'])
def add():
    info = request.form('bookInfo')

    book = Books(name=info['name'],
                 category=info['category'],
                 price=float(info['price']),
                 #user_id=request.user_id,
                 status=1
                 )
    db.session.add(book)
    db.session.commit()

    return redirect(url_for('index'))


# Select
@books.route('/books')
def books_all():
    books_all = Books.query().all()
    return jsonify(books_all)


@books.route('/<book_id>')
def book_info(book_id):
    book = Books.query().filter_by(Books.id == book_id)
    return jsonify(book)


# Update
@books.route('/<book_id>/update', methods=['POST'])
def update(book_id):
    pass


# Delete
@books.route('/<book_id>/delete', methods=['POST'])
def delete(book_id):
    book = Books.query().filter_by(Books.id == book_id)
    if book:
        db.session.delete(book)
        db.session.commit()
        return redirect(url_for('books_all'))
    else:
        abort(404)
