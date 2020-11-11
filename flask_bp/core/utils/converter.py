# _*_coding:utf-8_*_

"""
Project: python-fullstack
Author: Byron Hai
Date: 2020/11/2
"""
from werkzeug.routing import BaseConverter


class RegexConverter(BaseConverter):
    def __init__(self, url_map, *args):
        super(RegexConverter, self).__init__(url_map)
        self.regex = args[0]

    def to_python(self, value):
        return int(value) + 1

    def to_url(self, value):
        return super(RegexConverter, self).to_url(value)


class MobileConverter(BaseConverter):
    def __init__(self, url_map, *args):
        super(MobileConverter, self).__init__(url_map)
        self.regex = args[0]
