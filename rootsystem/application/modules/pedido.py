from cgi import FieldStorage
from time import strftime

from common.helpers import ControllerFactory
from core.db import DBQuery
from core.collector import Collector
from core.factory import Factory
from core.helpers import compose
from core.loglconnector import LoglConnector
from core.render import Template
from core.stdobject import StdObject
from modules.producto import Producto
from settings import ARG, db_data, HTTP_HTML, HOST, STATIC_PATH, TEMPLATE_PATH


class Pedido(object):

    def __init__(self):
        self.pedido_id = 0
        self.estado = 0
        self.fecha = ''
        self.cliente = 0
        #self.producto_collection = []

    def add_producto(self, producto):
        self.producto_collection.append(compose(producto, Producto))
    
    @staticmethod
    def get_pedidos(oid=0):
        sql = "SELECT pedido_id FROM pedido WHERE cliente = {}".format(oid)
        return DBQuery(db_data).execute(sql)
    
    def insert(self):
        sql = """
            INSERT INTO     pedido
                            (estado, fecha, cliente)
            VALUES          ({}, '{}', {})
        """.format(
            self.estado,
            self.fecha,
            self.cliente
        )
        self.pedido_id = DBQuery(db_data).execute(sql)

    def select(self):
        sql = """
            SELECT      estado, fecha, cliente
            FROM        pedido
            WHERE       pedido_id = {}
        """.format(self.pedido_id)
        resultados = DBQuery(db_data).execute(sql)[0]
        self.estado = resultados[0]
        self.fecha = resultados[1]
        self.cliente = resultados[2]

        if hasattr(self, 'producto_collection'):
            cl = LoglConnector(self, 'Producto')
            cl.select()

    def update(self):
        sql = """
            UDPATE      pedido
            SET         estado = {}, fecha = '{}', cliente = {}
            WHERE       pedido_id = {}
        """.format(
            self.estado,
            self.fecha,
            self.cliente,
            self.pedido_id
        )
        DBQuery(db_data).execute(sql)

    def delete(self):
        sql = "DELETE FROM pedido WHERE pedido_id = {}".format(self.pedido_id)
        DBQuery(db_data).execute(sql)


class PedidoView(object):

    def agregar(self, coleccion, cliente_id):
        pila = []
        tabla = Template(
            '{}/pedido_agregar.html'.format(STATIC_PATH)
        ).get_template()
        fila = Template(base=tabla).extract('producto')

        for producto in coleccion:
            diccionario = vars(producto)
            render = Template(base=fila).render(diccionario)
            pila.append(render)

        pila = ''.join(pila)
        contenido = tabla.replace(fila, pila)
        
        diccionario = dict(cliente=cliente_id)
        contenido = Template(base=contenido).render(diccionario)

        print(HTTP_HTML)
        print("")
        print(Template(TEMPLATE_PATH).render_inner(contenido))

    def ver(self, pedido, denominacion):
        ficha = Template(
            '{}/pedido_ver.html'.format(STATIC_PATH)).get_template()
        fila_producto = Template(base=ficha).extract('filapepro')
        pila = []
        total = []
        for producto in pedido.producto_collection:
            diccionario = vars(producto)
            diccionario['subtotal'] = producto.fm * producto.precio
            total.append(diccionario['subtotal'])
            render = Template(base=fila_producto).render(diccionario)
            pila.append(render)

        pila = ''.join(pila)
        contenido = ficha.replace(fila_producto, pila)

        cliente = Factory().make('Cliente', pedido.cliente)
        domicilio = cliente.domicilio
        diccionario = vars(pedido)
        diccionario.update(vars(domicilio))
        diccionario['denominacion'] = denominacion
        diccionario['total'] = sum(total)
        contenido = Template(base=contenido).render(diccionario)

        print(HTTP_HTML, "\n")
        print(Template(TEMPLATE_PATH).render_inner(contenido))


class PedidoController(object):

    def __init__(self):
        self.model = Pedido()
        self.view = PedidoView()

    def agregar(self):
        c = Collector()
        c.get("Producto")
        self.view.agregar(c.coleccion, ARG)

    def guardar(self):
        formulario = FieldStorage()
        productos = formulario['producto_id']
        cantidades = formulario['cantidad']
    
        self.model.estado = 1
        self.model.fecha = strftime("%Y-%m-%d")
        self.model.cliente = formulario['cliente'].value
        self.model.insert()
       
        self.model.producto_collection = []
        for i, elemento in enumerate(productos):
            pr = Producto()
            pr.producto_id = elemento.value
            pr.select()
            self.model.producto_collection.append(pr)
            pr.fm = cantidades[i].value

        cl = LoglConnector(self.model, 'Producto')
        cl.insert()
        
        print(HTTP_HTML)
        print("Location: {}/pedido/ver/{}".format(HOST, self.model.pedido_id))
        print("")

    def ver(self):
        self.model.pedido_id = int(ARG)
        self.model.producto_collection = []
        self.model.select()

        cliente_controller = ControllerFactory().make('ClienteController')
        cliente_controller.get_name(self.model.cliente)

        self.view.ver(self.model, cliente_controller.model.denominacion)
    
    def eliminar(self):
        self.model.pedido_id = int(ARG)
        self.model.select()
        cliente = Factory().make('Cliente', self.model.cliente)
        self.model.delete()
        
        print(HTTP_HTML)
        print("Location: {}/cliente/ver/{}".format(HOST, cliente.cliente_id))
        print("")
        print("")
