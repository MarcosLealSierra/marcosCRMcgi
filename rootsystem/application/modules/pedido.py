from cgi import FieldStorage
from time import strftime

from core.db import DBQuery
from core.helpers import compose
from core.loglconnector import LoglConnector
from core.render import Template
from core.stdobject import StdObject
from modules.producto import Producto
from settings import ARG, db_data, HTTP_HTML, HOST, STATIC_PATH, TEMPLATE_PATH


class Pedido(object):

    def __init__(self):
        self.pedido_id = 0
        self.estado = ''
        self.fecha = ''
        self.cliente = 0
        self.producto_collection = []

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
            VALUES          ('{}', '{}', {})
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

        cl = LoglConnector(self, 'Producto')
        cl.select()

    def update(self):
        sql = """
            UDPATE      pedido
            SET         estado = '{}', fecha = '{}', cliente = {}
            WHERE       pedido_id = {}
        """.format(
            self.estado,
            self.fecha,
            self.pedido_id
        )
        DBQuery(db_data).execute(sql)

    def delete(self):
        sql = "DELETE FROM pedido WHERE pedido_id = {}".format(self.pedido_id)
        DBQuery(db_data).execute(sql)


class PedidoView(object):

    def agregar(self):
        with open("{}/pedido_agregar.html".format(STATIC_PATH), "r") as f:
            form = f.read()

        print(HTTP_HTML)
        print("")
        print(form)

    def ver(self, pedido):
        with open("{}/pedido_ver.html".format(STATIC_PATH), "r") as f:
            ficha = f.read()

        diccionario = vars(pedido)
        ficha = Template(base=ficha).render(diccionario)

        print(HTTP_HTML)
        print("")
        print(Template(TEMPLATE_PATH).render_inner(ficha))


class PedidoController(object):

    def __init__(self):
        self.model = Pedido()
        self.view = PedidoView()

    def agregar(self):
        self.view.agregar()

    def guardar(self):
        formulario = FieldStorage()
        producto_id = formulario['producto_id']
        cantidad = formulario['cantidad']

        pd = Pedido()
        pd.estado = 1
        pd.fecha = strftime("%Y-%m-%d")
        pd.cliente = 1 
        pd.insert()
        
        for i, elemento in enumerate(producto_id):
            pr = Producto()
            pr.producto_id = elemento.value
            pr.select()
            pr.fm = cantidad[i].value
            pd.producto_collection.append(pr)

        cl = LoglConnector(pd, 'Producto')
        cl.insert()
        
        print(HTTP_HTML)
        print("Location: {}/pedido/ver/{}".format(HOST, pd.pedido_id))
        print("")
        print("")

    def ver(self):
        self.model.pedido_id = ARG
        self.model.select()

        self.view.ver(self.model)
