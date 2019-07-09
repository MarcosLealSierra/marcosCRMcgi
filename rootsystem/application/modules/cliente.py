from cgi import FieldStorage
from re import sub

from core.db import DBQuery
from core.collector import Collector
from core.helpers import compose
from core.render import Template
from core.stdobject import StdObject
from modules.domicilio import Domicilio
from modules.pedido import Pedido
from settings import ARG, db_data, HTTP_HTML, HTTP_REDIRECT, HOST, MODULE, \
    STATIC_PATH, TEMPLATE_PATH


class Cliente(StdObject):

    def __init__(self, domicilio=None):
        self.cliente_id = 0
        self.denominacion = ''
        self.nif = ''
        self.domicilio = compose(domicilio, Domicilio)
        #self.pedido_collection = []

    def add_pedido(self, pedido):
        self.pedido_collection.append(compose(pedido, Pedido))
    
    def select(self):
        super(Cliente, self).select()
        #pedido = Pedido()
        #pedidos = pedido.get_pedidos(self.cliente_id)

        #for tupla in pedidos:
            #pedido = Pedido()
            #pedido.pedido_id = tupla[0]
            #pedido.select()
            #self.pedido_collection.append(pedido)

        #print HTTP_HTML
        #print ""
        #print pedidos
        #print self.pedido_collection
        

class ClienteView(object):
    
    def agregar(self):
        with open("{}/cliente_agregar.html".format(STATIC_PATH), "r") as f:
            form = f.read()

        regex = "<!-- errores -->(.|\n)+<!-- errores -->"
        form = sub(regex, '', form)

        print(HTTP_HTML, "\n")
        print(Template(TEMPLATE_PATH).render_inner(form))
    
    def ver(self, cliente):
        with open("{}/cliente_ver.html".format(STATIC_PATH), "r") as f:
            ficha = f.read()

        diccionario = vars(cliente)
        diccionario.update(vars(cliente.domicilio))
        ficha = Template(base=ficha).render(diccionario)

        print(HTTP_HTML, "\n")
        print(Template(TEMPLATE_PATH).render_inner(ficha))

    def editar(self, cliente):
        with open("{}/cliente_editar.html".format(STATIC_PATH), "r") as f:
            form = f.read()

        regex = "<!-- errores -->(.|\n)+<!-- errores -->"
        ficha = sub(regex, '', form)

        diccionario = vars(cliente)
        diccionario.update(vars(cliente.domicilio))
        ficha = Template(base=ficha).render(diccionario)

        print(HTTP_HTML, "\n")
        print(Template(TEMPLATE_PATH).render_inner(ficha))

    def listar(self, coleccion):
        pila = []
        tabla = Template(
            '{}/cliente_listar.html'.format(STATIC_PATH)
        ).get_template()
        fila = Template(base=tabla).extract('fila')

        for cliente in coleccion:
            diccionario = vars(cliente)
            diccionario.update(vars(cliente.domicilio))
            render = Template(base=fila).render(diccionario)
            pila.append(render)

        pila = ''.join(pila)

        contenido = tabla.replace(fila, pila)

        print(HTTP_HTML, "\n")
        print(Template(TEMPLATE_PATH).render_inner(contenido))


class ClienteController(object):

    def __init__(self):
        self.model = Cliente()
        self.view = ClienteView()

    def agregar(self):
        self.view.agregar()

    def guardar(self):
        formulario = FieldStorage()

        self.model.domicilio = Domicilio()
        self.model.domicilio.calle = formulario['calle'].value
        self.model.domicilio.numero = formulario['numero'].value
        self.model.domicilio.planta = formulario['planta'].value
        self.model.domicilio.puerta = formulario['puerta'].value
        self.model.domicilio.ciudad = formulario['ciudad'].value
        self.model.domicilio.insert()
        
        self.model.denominacion = formulario['denominacion'].value
        self.model.nif = formulario['nif'].value
        self.model.insert()

        print(HTTP_HTML)
        print("Location: {}/cliente/ver/{}".format(HOST, self.model.cliente_id))
        print("")
        print("")

    def ver(self):
        self.model.cliente_id = int(ARG) 
        self.model.select()

        self.view.ver(self.model)

    def editar(self):
        self.model.cliente_id = int(ARG)
        self.model.select()
        
        self.view.editar(self.model)

    def actualizar(self):
        formulario = FieldStorage()
        self.model.cliente_id = formulario['cliente_id'].value
        self.model.select()
        self.model.nif = formulario['nif'].value
        self.model.denominacion = formulario['denominacion'].value

        self.model.domicilio.calle = formulario['calle'].value
        self.model.domicilio.numero = formulario['numero'].value
        self.model.domicilio.planta = formulario['planta'].value
        self.model.domicilio.puerta = formulario['puerta'].value
        self.model.domicilio.ciudad = formulario['ciudad'].value
        self.model.domicilio.update()

        self.model.update()
        
        print(HTTP_HTML)
        print("Location: {}/cliente/ver/{}".format(HOST, self.model.cliente_id))
        print("")
        print("")

    def eliminar(self):
        self.model.cliente_id = int(ARG)
        self.model.delete()
        
        print(HTTP_HTML)
        print("Location: {}/cliente/listar".format(HOST))
        print("")
        print("")

    def listar(self):
        c = Collector()
        c.get("Cliente")
        self.view.listar(c.coleccion)
