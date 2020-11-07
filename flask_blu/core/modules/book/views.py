# -*- coding: utf-8 -*-
# @File: views.py
# @Author: byron
# @Date: 11/7/20
from flask import request, redirect, jsonify
from core.modules.book import book_blu
from core.models import Book
from core.utils.common import login_check
from core.utils.status_code import response_code


@book_blu.route('/')
def get_books():
    books = Book.query.all()

    if books:
        books = [book.to_dict() for book in books]
        return jsonify(response_code.get_data_success(books))

    return jsonify(response_code.get_data_fail)


@book_blu.route('/<book_id>', methods=['POST'])
def get_book(book_id):
    book = Book.query.get(book_id)
    if book:
        return jsonify(response_code.get_data_success([book.to_dict()]))
    return jsonify(response_code.get_data_fail)


@book_blu.route('/add', methods=['POST'])
@login_check
def add():
    data = request.json
    name = data.get('name')
    category = data.get('category')
    price = data.get('price')
    # user_id = ""
    user_id = ""
    book = Book(name, category, price, user_id)
    book.add(book)
    return redirect(jsonify(response_code.success))


@book_blu.route('/<book_id>')
def book_info(book_id):
    book = Book.query.get(book_id)
    if book:
        return jsonify(response_code.get_data_success(book.to_dict()))
    return jsonify(book)


# Update
@book_blu.route('/<book_id>/update', methods=['POST'])
@login_check
def update(book_id):
    data = request.json
    name = data.get('name')
    category = data.get('category')
    price = data.get('price')

    book = Book.query.get(book_id)
    if book:
        if name:
            book.name = name
        if category:
            book.category = category

        if price:
            book.price = price
        book.update()

        book = Book.query.get(book_id)
        return jsonify(response_code.update_success(book.to_dict()))
    return jsonify(response_code.get_data_fail)


# Delete
@book_blu.route('/<book_id>/delete', methods=['POST'])
@login_check
def delete(book_id):
    book = Book.query.get(book_id)
    if book:
        book.delete()
        return jsonify(response_code.success)
    return jsonify(response_code.add_data_fail)
