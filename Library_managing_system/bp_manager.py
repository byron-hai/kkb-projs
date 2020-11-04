# _*_coding:utf-8_*_

"""
Project: python-fullstack
Author: Byron Hai
Date: 2020/11/2
"""

from flask_script import Manager
from bp_core import app, db

manager = Manager(app)

if __name__ == '__main__':
    app.run(debug=True)

