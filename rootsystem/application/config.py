#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cgi import FieldStorage


DEFAULT_RESOURCE = "/cliente/listar"  # Módulo y recurso por defecto
SHOW_ERROR_404 = False
STATIC_PATH = "/srv/websites/marcosCRMcgi/rootsystem/static"
TEMPLATE_PATH = "{}/template.html".format(STATIC_PATH)
PRIVATE_DIR = "/srv/websites/marcosCRMcgi/private"
CREDENTIAL_PATH = "{}/.credentials".format(PRIVATE_DIR)

DB_HOST = "localhost"
DB_USER = "marcoscrmcgi"
DB_PASS = "mysqlroot"
DB_NAME = "marcoscrmcgi"
db_data = [DB_HOST, DB_USER, DB_PASS, DB_NAME]

POST = FieldStorage()

author_data = {'AUTOR': 'Marcos Leal Sierra', 'ANCHOR': 'marcoslealsierra.com',
    'ANY': ''}

ERR_NUMERO_NO_VALIDO = """El número introducido no es válido"""

ERR_CALLE_NO_VALIDA = """
La calle introducida no es válida
"""

ERR_PLANTA_NO_VALIDA = """
La planta introducida no es válida
"""

ERR_PUERTA_NO_VALIDA = """
La puerta introducida no es válida
"""

ERR_CIUDAD_NO_VALIDA = """
La puerta introducida no es válida
"""
