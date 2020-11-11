# _*_coding:utf-8_*_

"""
Project: python-fullstack
Author: Byron Hai
Date: 2020/11/2
"""
import redis
import logging


class Config(object):
    DEBUG = True
    # os.urandom(24)
    SECRET_KEY = '\x93Y\xf9\xf4v\x1eK\xd5\xf5\x96\xa3]\xd7\x9d\xfaM\xeb\xf0\xef<z\x0b\x91\xd4'

    DIALECT = 'mysql'
    DRIVER = 'pymysql'

    USERNAME = 'root'
    PASSWORD = 'root1234'
    HOSTNAME = '127.0.0.1'
    PORT = '3306'
    DATABASE = 'flask_bp'

    URI = "{}+{}://{}:{}@{}:{}/{}".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
    SQLALCHEMY_DATABASE_URI = URI

    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SWAGGER_TITLE = "API"
    SWAGGER_DESC = "API 接口"
    SWAGGER_HOST = "localhost:5000"

    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = '6379'

    # SESSION_TYPE = "filesystem"
    SESSION_TYPE = "redis"  # assign session stored in redis
    SESSION_USE_SINGER = True  # make session_id in cookie encrypted
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    PERMANENT_SESSION_LIFETIME = 24 * 60 * 60  # session lifetime 24 hours

    LOG_LEVEL = logging.DEBUG


class DevelopmentConfig(Config):
    pass


class ProductionConfig(Config):
    DEBUG = False


class UnittestConfig(Config):
    TESTING = True


configs = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'test': UnittestConfig
}
