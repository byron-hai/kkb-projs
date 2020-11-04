# _*_coding:utf-8_*_

"""
Project: python-fullstack
Author: Byron Hai
Date: 2020/11/2
"""

DEBUG = True
DIALECT = 'mysql'
DRIVER = 'pymysql'

SQL = 'mysqldb'
USERNAME = 'root'
PASSWORD = '123456'
HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'library_db'

URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf-8".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = URI

SQLALCHEMY_TRACK_MODIFICATIONS = True
SWAGGER_TITLE = "API"
SWAGGER_DESC = "API 接口"
SWAGGER_HOST = "localhost:5000"

