# -*- coding: utf-8 -*-
# @File: user_api.py
# @Author: byron
# @Date: 11/9/20
from flask import jsonify
from flask_restful import Resource, reqparse
from manager import db
from core.models import User

req_parser = reqparse.RequestParser()
req_parser.add_argument('username', dest='username', location='json', help='User name')
req_parser.add_argument('mobile', dest='mobile', location='json',
                        required=True, help="User's mobile")
req_parser.add_argument('password', dest="password", location='json',
                        required=True, help="Login password")


class UsersApi(Resource):
    def get(self):
        users = User.query.all()
        if users:
            data = {
                'code': '0',
                'msg': 'success',
                'data': [user.to_dict() for user in users]
            }
            return jsonify(data)
        return jsonify({'code': '-1', 'msg': 'No data found'})

    def post(self):
        args = req_parser.parse_args()
        user = User(nickname=args.username, mobile=args.mobile, passwd=args.password)
        db.session.add(user)
        user.session_commit()
        return "add a new user"


class UserApi(Resource):
    def get(self, user_id):
        user = User.query.get(user_id)
        if user:
            data = {
                'code': '0',
                'msg': 'success',
                'data': user.to_dict()
            }
            return jsonify(data)
        return jsonify({'code': '-1', 'msg': 'No data found'})

    def patch(self, user_id):
        args = req_parser.parse_args()
        nickname = args.username
        mobile = args.mobile
        passwd = args.password

        user = User.query.get(user_id)
        if user:
            if nickname:
                user.nickname = nickname
            if mobile:
                user.mobile = mobile
            if passwd:
                user._password = passwd

            err = user.session_commit()

            if not err:
                user = User.query.get(user_id)
                return jsonify({'code': '0', 'msg': 'success', 'data': user.to_dict()})
            return jsonify({'code': '-1', 'msg': 'Update user failed', 'error': err})
        return jsonify({'code': '-1', 'msg': "user %s not found" % user_id})

    def delete(self, user_id):
        user = User.query.get(user_id)
        db.session.delete(user)
        user.session_commit()

        if not User.query.get(user_id):
            return jsonify({'code': '0', 'msg': 'success'})
        return jsonify({'code': '-1', 'msg': "delete user: %s failed" % user_id})

