from cgi import FieldStorage
from re import sub

from core.db import DBQuery
from core.collector import Collector
from core.controller import Controller
from core.render import Template
from core.stdobject import StdObject
from settings import ARG, db_data, HTTP_HTML, HTTP_REDIRECT, HOST, MODULE, \
    STATIC_PATH, TEMPLATE_PATH


class Producto(StdObject):

    def __init__(self):
        self.producto_id = 0
        self.denominacion = ''
        self.precio = 0.0
    
    def insert(self):
        sql = """
            INSERT INTO     producto
                            (denominacion, precio)
            VALUES          ('{}', {})
        """.format(
            self.denominacion,
            self.precio,
        )
        self.producto_id = DBQuery(db_data).execute(sql)

    def update(self):
        sql = """
            UPDATE      producto
            SET         denominacion = '{}', precio = {}
            WHERE       producto_id = {}
        """.format(
            self.denominacion,
            self.precio,
            self.producto_id
        )
        DBQuery(db_data).execute(sql)

class ProductoView(object):

    def agregar(self):
        with open("{}/producto_agregar.html".format(STATIC_PATH), "r") as f:
            form = f.read()

        regex = "<!-- errores -->(.|\n)+<!-- errores -->"
        form = sub(regex, '', form)

        print(HTTP_HTML)
        print("")
        print(Template(TEMPLATE_PATH).render_inner(form))

    def ver(self, producto):
        with open("{}/producto_ver.html".format(STATIC_PATH), "r") as f:
            ficha = f.read()

        diccionario = vars(producto)
        ficha = Template(base=ficha).render(diccionario)

        print(HTTP_HTML)
        print("")
        print(Template(TEMPLATE_PATH).render_inner(ficha))

    def editar(self, producto):
        with open("{}/producto_editar.html".format(STATIC_PATH), "r") as f:
            form = f.read()

        regex = "<!-- errores -->(.|\n)+<!-- errores -->"
        ficha = sub(regex, '', form)

        diccionario = vars(producto)
        ficha = Template(base=ficha).render(diccionario)

        print(HTTP_HTML)
        print("")
        print(Template(TEMPLATE_PATH).render_inner(ficha))

    def listar(self, coleccion):
        pila = []
        tabla = Template(
            '{}/producto_listar.html'.format(STATIC_PATH)
        ).get_template()
        fila = Template(base=tabla).extract('fila')

        for producto in coleccion:
            diccionario = vars(producto)
            render = Template(base=fila).render(diccionario)
            pila.append(render)

        pila = ''.join(pila)

        contenido = tabla.replace(fila, pila)

        print(HTTP_HTML)
        print("")
        print(Template(TEMPLATE_PATH).render_inner(contenido))


class ProductoController(Controller):

    def agregar(self):
        self.view.agregar()

    def guardar(self):
        formulario = FieldStorage()
        self.model.denominacion = formulario['denominacion'].value
        self.model.precio = formulario['precio'].value
        self.model.insert()

        print(HTTP_HTML)
        print("Location: {}/producto/ver/{}".format(HOST, self.model.producto_id))
        print("")
        print("")

    def ver(self):
        self.model.producto_id = ARG 
        self.model.select()

        self.view.ver(self.model)

    def editar(self):
        self.model.producto_id = ARG
        self.model.select()
        
        self.view.editar(self.model)

    def actualizar(self):
        formulario = FieldStorage()
        self.model.producto_id = formulario['producto_id'].value
        self.model.denominacion = formulario['denominacion'].value
        self.model.precio = formulario['precio'].value
        self.model.update()
        
        print(HTTP_HTML)
        print("Location: {}/producto/ver/{}".format(HOST, self.model.producto_id))
        print("")
        print("")

    def eliminar(self):
        self.model.producto_id = ARG
        self.model.delete()
        
        print(HTTP_HTML)
        print("Location: {}/producto/listar".format(HOST))
        print("")
        print("")

    def listar(self):
        c = Collector()
        c.get("Producto")	
        self.view.listar(c.coleccion)
