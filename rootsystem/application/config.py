#!/usr/bin/env python
# -*- coding: utf-8 -*-


DEFAULT_RESOURCE = "/cliente/listar"  # Módulo y recurso por defecto
SHOW_ERROR_404 = False
STATIC_PATH = "/home/mleal/src/proyectos/marcosCRMcgi/rootsystem/static"
TEMPLATE_PATH = "{}/template.html".format(STATIC_PATH)

DB_HOST = "localhost" 
DB_USER = "marcoscrmcgi"
DB_PASS = "mysqlroot"
DB_NAME = "marcoscrmcgi"
db_data = [DB_HOST, DB_USER, DB_PASS, DB_NAME]

author_data = {'AUTOR': 'Marcos Leal Sierra', 'ANCHOR': 'marcoslealsierra.com',
    'ANY': ''}
