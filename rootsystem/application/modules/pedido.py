from cgi import FieldStorage

from core.db import DBQuery
from core.helpers import compose
from core.loglconnector import LoglConnector
from core.render import Template
#from core.stdobject import StdObject
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

    @staticmethod
    def get_pedidos(oid=0):
        sql = "SELECT pedido_id FROM pedido WHERE cliente = {}".format(oid)
        return DBQuery(db_data).execute(sql)


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

        #print(HTTP_HTML)
        #print("")
        #for i, elemento in enumerate(producto_id):
            #p = Producto()
            #p.producto_id = elemento.value
            #p.select()
            #p.fm = cantidad[i].value
            #print(vars(p))

        pd = Pedido()
        pd.cliente = 2 
        pd.insert()
        
        for i, elemento in enumerate(producto_id):
            pr = Producto()
            pr.producto_id = elemento.value
            pr.select()
            pr.fm = cantidad[i].value
            pd.producto_collection.append(pr)
            


	# controlador PEDIDO
	#pr16 = Producto()
	#pr16.producto_id = 26
        #pr16.select()
	#pd.producto_collection.append(pr16)
	#pr16.fm = 100

	#pr23 = Producto()
	#pr23.producto_id = 27
        #pr23.select()
	#pd.producto_collection.append(pr23)
	#pr23.fm = 50

	#pr72 = Producto()
	#pr72.producto_id = 28
        #pr72.select()
	#pd.producto_collection.append(pr72)
	#pr72.fm = 25

        cl = LoglConnector(pd, 'Producto')
        cl.insert()
        
        #print(HTTP_HTML)
        #print("")
        #print(vars(cl))
        
        print(HTTP_HTML)
        print("Location: {}/pedido/ver/{}".format(HOST, self.model.pedido_id))
        print("")
        print("")

    def ver(self):
        self.model.pedido_id = ARG
        self.model.select()

        self.view.ver(self.model)

        #print(HTTP_HTML)
        #print("")
        #print(vars(self.model))
