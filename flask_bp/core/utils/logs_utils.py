# -*- coding: utf-8 -*-
# @File: logs_utils.py
# @Author: byron
# @Date: 11/11/20
import logging
from logging.handlers import RotatingFileHandler
from config.config import configs


def setup_log(config_name):
    logging.basicConfig(level=configs[config_name].LOG_LEVEL)
    log_file_handler = RotatingFileHandler("logs/log",
                                           maxBytes=1024 * 1024 * 100,
                                           backupCount=10)
    formatter = logging.Formatter('%(levelname)s %(filename)s: %(lineno)d %(message)?')
    log_file_handler.setFormatter(formatter)
    logging.getLogger().addHandler(log_file_handler)
