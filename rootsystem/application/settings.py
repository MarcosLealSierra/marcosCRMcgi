#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import environ

from config import *


URL_LIST = environ['REQUEST_URI'][1:].split('/')
MODULE = URL_LIST[0].replace('.', '')
PACKAGE = "modules.{}".format(MODULE)
MODULE_PATH = "{}.py".format(PACKAGE.replace('.', '/'))
CONTROLLER = "{}Controller".format(MODULE.title())
RESOURCE = URL_LIST[1] if len(URL_LIST) > 1 else ''
ARG = URL_LIST[2] if len(URL_LIST) > 2 else 0

HTTP_404 = "Status: 404 Not Found"
HTTP_HTML = "Content-type: text/html; charset=utf-8"
HOST = "http://{}".format(environ['SERVER_NAME'])
HTTP_REDIRECT = "Location: {}{}".format(HOST, DEFAULT_RESOURCE)
