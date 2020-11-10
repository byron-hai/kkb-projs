# -*- coding: utf-8 -*-
# @File: book_api.py
# @Author: byron
# @Date: 11/7/20
from flask import request, jsonify
from flask_restful import Resource
from core.models import Book
from core import db


class BooksApi(Resource):
    def get(self):
        """
        Get all books
        :return:
        """
        books = Book.query.all()
        if books:
            books = [book.to_dict() for book in books]
            return jsonify({'code': '0', 'msg': 'success', 'data': books})

        return jsonify(code='-1', msg="No records found")

    # @login_check
    def post(self):
        data = request.json
        name = data.get('name')
        category = data.get('category')
        price = data.get('price')
        user_id = 1  # Todo: Get user_id from cookie

        is_exist = Book.query.filter_by(name=name).first()
        if is_exist:
            jsonify({'code': '-1', 'msg': "Add books failed", 'error': "books with this name existed"})

        book = Book(name, category, price, user_id)
        db.session.add(book)
        err = book.session_commit()

        if not err:
            book = Book.query.filter_by(name=name).first()
            return jsonify({'code': '0', 'data': book.to_dict(), 'msg': 'success'})
        return jsonify({'code': '-1', 'msg': 'add books failed', 'error': err})


class BookApi(Resource):
    def get(self, book_id):
        book = Book.query.get(book_id)
        if book:
            return jsonify({'code': '0', 'message': 'success', 'data': book.to_dict()})
        return jsonify({'code': '-1', 'msg': 'No records found'})

    # @login_check
    def patch(self, book_id):
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
            err = book.session_commit()

            if not err:
                book = Book.query.get(book_id)
                return jsonify({'code': '0', 'msg': 'success', 'data': book.to_dict()})
            return jsonify({'code': '-1', 'msg': 'update books info failed', 'error': err})
        return jsonify({'code': '-1', 'msg': 'get books failed'})

    # @login_check
    def delete(self, book_id):
        book = Book.query.get(book_id)
        if book:
            book.status = '1'
            err = book.session_commit()

            if not err:
                book = Book.query.get(book_id)
                return jsonify({'code': '0', 'msg': 'success', 'data': book.to_dict()})
            return jsonify({'code': '-1', 'msg': 'delete failed'})
        return jsonify({'code': '-1', 'msg': 'books not found'})
