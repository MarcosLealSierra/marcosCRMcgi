from cgi import FieldStorage
from re import sub

from core.db import DBQuery
from core.collector import Collector
from core.helpers import compose
from core.factory import Factory
from core.render import Template
from core.stdobject import StdObject
from modules.datodecontacto import DatoDeContacto, DatoDeContactoController
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
        self.datodecontacto_collection = []
        self.pedido_collection = []
    
    def add_datodecontacto(self, datodecontacto):
        self.datodecontacto_collection.append(compose(datodecontacto, DatoDeContacto))

    def add_pedido(self, pedido):
        self.pedido_collection.append(compose(pedido, Pedido))
    
    def get_name(self, idc=0):
        self.model.cliente_id = idc
        self.model.select()

    def insert(self):
        sql = """
            insert into     cliente
                            (denominacion, nif, domicilio)
            values          ('{}', '{}', {})
        """.format(
            self.denominacion,
            self.nif,
            self.domicilio.domicilio_id
        )
        self.cliente_id = DBQuery(db_data).execute(sql)
    
    def select(self):
        super(Cliente, self).select()
       
        pedidos = Pedido.get_pedidos(self.cliente_id)
        for tupla in pedidos:
            pedido = Pedido()
            pedido.pedido_id = tupla[0]
            pedido.select()
            self.add_pedido(pedido)

        datosdecontacto = DatoDeContacto.get_datosdecontacto(self.cliente_id)
        for tupla in datosdecontacto:
            datodecontacto = DatoDeContacto()
            datodecontacto.datodecontacto_id = tupla[0]
            datodecontacto.select()
            self.add_datodecontacto(datodecontacto)

    def update(self):
        sql = """
            UPDATE      cliente
            SET         denominacion = '{}', nif = '{}', domicilio = {}
            WHERE       cliente_id = {}
        """.format(
            self.denominacion,
            self.nif,
            self.domicilio.domicilio_id,
            self.cliente_id
        )
        DBQuery(db_data).execute(sql)


class ClienteView(object):
    
    def agregar(self):
        with open("{}/cliente_agregar.html".format(STATIC_PATH), "r") as f:
            form = f.read()

        regex = "<!-- errores -->(.|\n)+<!-- errores -->"
        form = sub(regex, '', form)

        print(HTTP_HTML, "\n")
        print(Template(TEMPLATE_PATH).render_inner(form))
    
    def ver(self, cliente):
        ficha = Template(
            '{}/cliente_ver.html'.format(STATIC_PATH)).get_template()

        fila_dc = Template(base=ficha).extract('fila_dc')
        pila = []
        for dc in cliente.datodecontacto_collection:
            diccionario = vars(dc)
            render = Template(base=fila_dc).render(diccionario)
            pila.append(render)

        pila = ''.join(pila)
        ficha = ficha.replace(fila_dc, pila)

        fila_pedido = Template(base=ficha).extract('fila_hp')
        pila = []
        for pedido in cliente.pedido_collection:
            diccionario = vars(pedido)
            render = Template(base=fila_pedido).render(diccionario)
            pila.append(render)

        pila = ''.join(pila)
        ficha = ficha.replace(fila_pedido, pila)

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

    def get_name(self, idc=0):
        self.model.cliente_id = idc
        self.model.select()

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

        dc = DatoDeContactoController()
        dc.guardar(formulario, self.model.cliente_id)

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
