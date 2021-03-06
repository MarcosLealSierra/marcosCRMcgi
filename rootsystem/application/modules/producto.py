from re import sub

from core.db import DBQuery
from core.collector import Collector
from core.controller import Controller
from core.helpers import redirect, get_form_value
from core.render import Template
from core.sessions import Sessions
from core.stdobject import StdObject
from settings import ARG, db_data, HTTP_HTML, HTTP_REDIRECT, HOST, MODULE, \
    POST, STATIC_PATH, TEMPLATE_PATH


class Producto(StdObject):

    def __init__(self):
        self.producto_id = 0
        self.denominacion = ''
        self.precio = 0.0

    def insert(self):
        sql = """
            INSERT INTO producto
            (denominacion, precio)
            VALUES ('{}', {})
        """.format(
            self.denominacion,
            self.precio,
        )
        self.producto_id = DBQuery().execute(sql)

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
        archivo = '{}/producto_listar.html'.format(STATIC_PATH)
        contenido = Template(archivo).render_dict(coleccion, tag="fila")
        contenido = Template(TEMPLATE_PATH).render_inner(contenido)
        Template.print(contenido)


class ProductoController(Controller):

    def agregar(self):
        self.view.agregar()

    def guardar(self):
        denominacion = POST['denominacion'].value
        precio = POST['precio'].value

        self.model.denominacion = denominacion
        self.model.precio = precio
        self.model.insert()

        redirect("producto/ver/{}".format(self.model.producto_id))

    def ver(self):
        self.model.producto_id = ARG
        self.model.select()

        self.view.ver(self.model)

    def editar(self):
        self.model.producto_id = ARG
        self.model.select()

        self.view.editar(self.model)

    def actualizar(self):
        producto_id = get_form_value('producto_id')
        denominacion = get_form_value('denominacion')
        precio = get_form_value('precio')

        self.model.producto_id = producto_id
        self.model.denominacion = denominacion
        self.model.precio = precio
        self.model.update()

        redirect("producto/ver/{}".format(self.model.producto_id))

    def eliminar(self):
        self.model.producto_id = ARG
        self.model.delete()

        redirect("producto/listar")

    def listar(self):
        #Sessions.check()
        c = Collector()
        c.get("Producto")
        self.view.listar(c.coleccion)
