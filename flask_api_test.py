# -*- coding: utf-8 -*-
# @File: flask_api_test.py
# @Author: byron
# @Date: 11/10/20

import sys
import pymysql
import requests
import logging

LOG_FMT = "%(message)s"
logging.basicConfig(level=logging.DEBUG, format=LOG_FMT)


def init_db(db_name):
    hostname = '127.0.0.1'
    username = 'root'
    password = 'root1234'
    database = db_name

    logger.info("database name: " + db_name)
    db = pymysql.connect(host=hostname, user=username, password=password, db=database)
    cursor = db.cursor()
    cursor.execute("use " + database)
    cursor.execute("show tables")
    logger.info("database name: " + db_name)
    logger.info("Tables in database:")
    outputs = cursor.fetchall()
    for out in outputs:
        logger.debug(out)

    logger.info("Truncate tables")
    cursor.execute("truncate users")

    cursor.execute("select * from users")
    outputs = cursor.fetchall()
    for out in outputs:
        logger.debug(out)

    cursor.execute("truncate books")
    cursor.execute("select * from books")
    outputs = cursor.fetchall()
    for out in outputs:
        logger.debug(out)

    db.close()


class ApiTest(object):
    def tc_register(self, url):
        user_list = [("User-001", "12345678001", "123456"),
                     ("User-002", "12345678002", "123456")]

        for user in user_list:
            json_data = {"username": user[0], "mobile": user[1], "password": user[2]}
            logger.debug("user info: %s", json_data)
            resp = requests.post(url, json=json_data)
            logger.debug("Request response:\n" + resp.text)

            if resp.json()['code'] != '0':
                logger.error(f"Test failed for: {url}")
                return False

    def tc_login(self, url):
        user = ("User-001", "12345678001", "123456")
        json_data = {"username": user[0], "mobile": user[1], "password": user[2]}
        logging.debug("user info: %s", json_data)
        resp = requests.post(url, json=json_data)
        logger.debug("Request response:\n" + resp.text)

        if resp.json()['code'] != '0':
            logger.error(f"Test failed for: {url}")

    def tc_add_book(self, url):
        book_list = [("Python", "IT", "56"),
                     ("Flask", "IT", "46")]

        for book in book_list:
            json_data = {"name": book[0], "category": book[1], "price": book[2]}
            logging.debug("book info: %s", json_data)
            resp = requests.post(url, json=json_data)
            logger.debug("Request response:\n" + resp.text)

            if resp.json()['code'] != '0':
                logger.error(f"Test failed for: {url}")
                return False

    def tc_get_books(self, url):
        resp = requests.get(url)
        logger.debug("Request response:\n" + resp.text)
   
        if resp.json()['code'] != '0':
            logger.error(f"Test failed for: {url}")

    def tc_get_book(self, url):
        resp = requests.get(url)
        logger.debug("Request response:\n" + resp.text)
        
        if resp.json()['code'] != '0':
            logger.error(f"Test failed for: {url}")

    def tc_update_books(self, url):
        logger.info("Before update")
        logger.debug(requests.get(url).text)
        book = ("Flask", "IT", "36")
        logging.info("Update item: book price")
        json_data = {"name": book[0], "category": book[1], "price": book[2]}
        
        resp = requests.patch(url, json=json_data)
        logger.info("\nAfter update")
        logger.debug("Request response:\n" + resp.text)

        if resp.json()['code'] != '0':
            logger.error(f"Test failed for: {url}")

    def tc_delete_books(self, url):
        resp = requests.delete(url)
        logger.debug("Request response:\n" + resp.text)
        
        if resp.json()['code'] != '0':
            logger.error(f"Test failed for: {url}")


def run_test(tc_api_list, api_dict):
    """
    dict-demo:
        "register": "/passport/register",
        "login": "/passport/login",
        "get_books": "/books",
        "add_book": "/books/book",
        "get_book": "/books/book/1",
        "update_book": "/books/book/2",
        "delete_book": "/books/book/2"
    """
    base_url = "http://127.0.0.1:5000"
    tc = ApiTest()

    api_func_map = {
        'register': tc.tc_register,
        'login': tc.tc_login,
        'get_books': tc.tc_get_books,
        'add_book': tc.tc_add_book,
        'get_book': tc.tc_get_book,
        'update_book': tc.tc_update_books,
        'delete_book': tc.tc_delete_books
    }

    for api in tc_api_list:
        tc_api = api_dict.get(api)
        tc_func = api_func_map.get(api)
        if not tc_api:
            logger.warning(f"Testing API: {api} not found")

        if not tc_func:
            logger.warning(f"Testing function not found for {api}")

        tc_api = base_url + tc_api
        logger.info(f"\nTesting item: {api}\nTesting API: " + tc_api)
        tc_func(tc_api)


if __name__ == "__main__":

    api_dict = {
        "flask_basic": {
            "register": "/passport/register",
            "login": "/passport/login",
            "get_books": "/books",
            "add_book": "/books/book",
            "get_book": "/books/book/1",
            "update_book": "/books/book/2",
            "delete_book": "/books/book/2"
        },

        "flask_bp": {
            "register": "/passport/register",
            "login": "/passport/login",
            "get_books": "/books/",
            "add_book": "/books/book",
            "get_book": "/books/book/1",
            "update_book": "/books/book/2",
            "delete_book": "/books/book/2"
        },

        "flask_rp": {
            "register": "/v1/passport/register",
            "login": "/v1/passport/login",
            "get_books": "/v1/books/",
            "add_book": "/v1/books/book",
            "get_book": "/v1/books/book/1",
            "update_book": "/v1/books/book/2",
            "delete_book": "/v1/books/book/2"
        },

        "flask_restful": {
            "register": "/passport/register",
            "login": "/passport/login",
            "get_books": "/books",
            "add_book": "/books/book",
            "get_book": "/books/book/1",
            "update_book": "/books/book/2",
            "delete_book": "/books/book/2"
        },

        "flask_bp_rest": {
            "register": "/passport/register",
            "login": "/passport/login",
            "get_books": "/books",
            "add_book": "/books/book",
            "get_book": "/books/book/1",
            "update_book": "/books/book/2",
            "delete_book": "/books/book/2"
        }
    }

    db_map = {
        "flask_basic": "flask_basic",
        "flask_bp": "flask_blu",
        "flask_rp": "library_db",
        "flask_restful": "flask_restful",
        "flask_bp_rest": "flask_bp_restful"
    }

    if len(sys.argv) == 1:
        logger.info("project name not defined")
        exit()

    tc_proj = sys.argv[1]
    log_name = tc_proj + "_test.log"
    handler = logging.FileHandler(log_name)
    logger = logging.getLogger(__name__)
    logger.addHandler(handler)
    
    logger.info(f"{'*' * 30} Testing Info {'*' * 30}")
    logger.info("\nProject Name: " + tc_proj)
    tc_api_dict = api_dict[tc_proj]
    logger.info("Testing APIs: ")

    for k, v in tc_api_dict.items():
        logger.info(f"{k:20s}: {v:40s}")

    logger.info(f"\n{'*' * 30} Init Database {'*' * 30}")
    init_db(db_map[tc_proj])

    logger.info(f"\n{'*' * 30} Starting Test {'*' * 30}")
    api_list = ["register", "login", "add_book", "get_books",
                "get_book", "update_book", "delete_book"]
    run_test(api_list, tc_api_dict)

    with open(log_name, 'rt') as fr:
        content = fr.read()

    if "fail" in content:
        logger.error("**** Testing failed ****")
        exit(-1)
    logger.info("**** All cases test passed ****")
    exit(0)

