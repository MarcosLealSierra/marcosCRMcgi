#!/usr/bin/env python
# -*- coding: utf-8 -*-

from settings import HTTP_HTML


class Producto(object):
    pass


class ProductoView(object):

    def vista(self):
        print HTTP_HTML
        print ""
        print "Hola Mundo"


class ProductoController(object):
    
    def __init__(self):
        self.model = Producto()
        self.view = ProductoView()
    
    def recurso(self):
        self.view.vista()
