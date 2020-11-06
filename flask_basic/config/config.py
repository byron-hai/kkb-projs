# _*_coding:utf-8_*_

"""
Project: python-fullstack
Author: Byron Hai
Date: 2020/11/2
"""
import os


base_dir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = True
    SECRET_KEY = 'Todo: need change'

    DIALECT = 'mysql'
    DRIVER = 'pymysql'

    USERNAME = 'root'
    PASSWORD = 'root1234'
    HOSTNAME = '127.0.0.1'
    PORT = '3306'
    DATABASE = 'flask_basic'

    URI = "{}+{}://{}:{}@{}:{}/{}".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
    SQLALCHEMY_DATABASE_URI = URI

    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SWAGGER_TITLE = "API"
    SWAGGER_DESC = "API 接口"
    SWAGGER_HOST = "localhost:5000"

