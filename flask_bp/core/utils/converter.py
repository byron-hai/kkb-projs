# _*_coding:utf-8_*_

"""
Project: python-fullstack
Author: Byron Hai
Date: 2020/11/2
"""
from werkzeug.routing import BaseConverter


class RegexConverter(BaseConverter):
    def __init__(self, url_map, *args):
        super().__init__(url_map)
        self.regex = args[0]

    def to_python(self, value):
        return value

    def to_url(self, value):
        return super(RegexConverter, self).to_url(value)


class MobileConverter(BaseConverter):
    def __init__(self, url_map, *args):
        super().__init__(url_map)
        self.regex = r'1[35678]\d{9}'
