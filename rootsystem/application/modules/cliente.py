from re import sub

from core.db import DBQuery
from core.collector import Collector
from core.helpers import compose, get_form_value, redirect, Sanitizer
from core.factory import Factory
from core.render import Template
from core.sessions import Sessions
from core.stdobject import StdObject
from modules.datodecontacto import DatoDeContacto, DatoDeContactoController
from modules.domicilio import Domicilio
from modules.pedido import Pedido
from settings import ARG, db_data, ERR_CALLE_NO_VALIDA, ERR_NUMERO_NO_VALIDO, \
    ERR_PLANTA_NO_VALIDA, ERR_PUERTA_NO_VALIDA, ERR_CIUDAD_NO_VALIDA, \
    HTTP_HTML, HTTP_REDIRECT, HOST, MODULE, POST, STATIC_PATH, TEMPLATE_PATH


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

    def insert(self):
        sql = """
            INSERT INTO cliente
            (denominacion, nif, domicilio)
            VALUES ('{}', '{}', {})
        """.format(
            self.denominacion,
            self.nif,
            self.domicilio.domicilio_id
        )
        self.cliente_id = DBQuery().execute(sql)

    def select(self, producto_collection=False):
        super(Cliente, self).select()

        pedidos = Pedido.get_pedidos(self.cliente_id)
        for tupla in pedidos:
            pedido = Pedido()
            pedido.pedido_id = tupla[0]
            if producto_collection:
                pedido.producto_collection = []
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

    def agregar(self, errores=[], fields={}):
        errores = "<br>".join(errores)
        with open("{}/cliente_agregar.html".format(STATIC_PATH), "r") as f:
            form = f.read()

        dictionary = dict()
        dictionary['errores'] = errores
        dictionary['calle'] = get_form_value("calle")
        dictionary['numero'] = get_form_value("numero")
        dictionary['puerta'] = get_form_value("puerta")
        dictionary['ciudad'] = get_form_value("ciudad")
        dictionary['planta'] = get_form_value("planta")
        dictionary['denominacion'] = get_form_value("denominacion")
        dictionary['nif'] = get_form_value("nif")

        if not errores:
            regex = "<!-- errores -->(.|\n)+<!-- errores -->"
            form = sub(regex, '', form)

        form = Template(base=form).render(dictionary)

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
            pedido.cantidad = len(pedido.producto_collection)
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
        #calle = Sanitizer.filter_string(POST['calle'].value)
        #ciudad = Sanitizer.filter_string(POST['ciudad'].value)
        #denominacion = Sanitizer.filter_string(POST['denominacion'].value)
        #numero = Sanitizer.convert_to_int(POST['numero'].value)
        #planta = Sanitizer.convert_to_int(POST['planta'].value)
        #puerta = Sanitizer.purge_alnum(POST['puerta'].value).upper()
        #nif = POST['nif'].value
        calle = POST['calle'].value
        ciudad = POST['ciudad'].value
        denominacion = POST['denominacion'].value
        numero = POST['numero'].value
        planta = POST['planta'].value
        puerta = POST['puerta'].value.upper()
        nif = POST['nif'].value

        errores = []

        if not (numero >= 1 and numero <= 15000):
            errores.append(ERR_NUMERO_NO_VALIDO)

        if not (planta >= 0 and planta <= 200):
            errores.append(ERR_PLANTA_NO_VALIDA)

        if not (len(puerta) >= 1 and len(puerta) <= 2):
            errores.append(ERR_PUERTA_NO_VALIDA)

        if not (len(calle) >= 1 and len(calle) <= 50):
            errores.append(ERR_CALLE_NO_VALIDA)

        if not (len(ciudad) >= 4 and len(calle) <= 30):
            errores.append(ERR_CIUDAD_NO_VALIDA)

        if errores:
            variables = locals()
            for k in POST.keys():
                if k in variables: POST[k].value = locals()[k]
            self.view.agregar(errores, POST)
            exit()

        self.model.domicilio = Domicilio()
        self.model.domicilio.calle = calle
        self.model.domicilio.numero = numero
        self.model.domicilio.planta = planta
        self.model.domicilio.puerta = puerta
        self.model.domicilio.ciudad = ciudad
        self.model.domicilio.insert()

        self.model.denominacion = denominacion
        self.model.nif = nif
        self.model.insert()

        dc = DatoDeContactoController()
        dc.guardar(POST, self.model.cliente_id)

        redirect("cliente/ver/{}".format(self.model.cliente_id))

    def ver(self):
        self.model.cliente_id = int(ARG)
        self.model.select(producto_collection=True)

        self.view.ver(self.model)

    def editar(self):
        self.model.cliente_id = int(ARG)
        self.model.select()

        self.view.editar(self.model)

    def actualizar(self):
        formulario = FieldStorage()

        cliente_id = formulario['cliente_id'].value
        nif = formulario['nif'].value
        denominacion = formulario['denominacion'].value

        domicilio.calle = formulario['calle'].value
        domicilio.numero = formulario['numero'].value
        domicilio.planta = formulario['planta'].value
        domicilio.puerta = formulario['puerta'].value
        domicilio.ciudad = formulario['ciudad'].value

        self.model.cliente_id = cliente_id
        self.model.select()
        self.model.nif = nif
        self.model.denominacion = denominacion

        self.model.domicilio.calle = calle
        self.model.domicilio.numero = numero
        self.model.domicilio.planta = planta
        self.model.domicilio.puerta = puerta
        self.model.domicilio.ciudad = ciudad
        self.model.domicilio.update()

        self.model.update()

        redirect("cliente/ver", self.model.cliente_id)

    def eliminar(self):
        self.model.cliente_id = int(ARG)
        self.model.delete()

        redirect("cliente/listar")

    def listar(self):
        Sessions.check()
        c = Collector()
        c.get("Cliente")
        self.view.listar(c.coleccion)
