from cgi import FieldStorage
from re import sub

from core.db import DBQuery
from core.collector import Collector
from core.render import Template
from domicilio import Domicilio
from settings import ARG, db_data, HTTP_HTML, HTTP_REDIRECT, HOST, MODULE, \
        STATIC_PATH, TEMPLATE_PATH


class Cliente(object):        # compuesto: se compone de...

    def __init__(self):
        self.cliente_id = 0
        self.denominacion = ''
	self.nif = ''
        self.domicilio = Domicilio()
    
    def insert(self):       # = update
        sql = """
            INSERT INTO cliente (denominacion, nif, domicilio) 
            VALUES            ('{}', '{}', {})
        """.format(self.denominacion, self.nif, self.domicilio.domicilio_id)
        self.cliente_id = DBQuery(db_data).execute(sql)

    def select(self):
        sql = """
            SELECT  denominacion, nif, domicilio 
            FROM    cliente 
            WHERE   cliente_id = {}
        """.format(self.cliente_id)
        resultados = DBQuery(db_data).execute(sql)[0]
        self.denominacion = resultados[0]
	self.nif = resultados[1]
        self.domicilio.domicilio_id = resultados[2]
        self.domicilio.select()
    
    def update(self):
        sql = """
            UPDATE      cliente
            SET         denominacion = '{}', nif = '{}', domicilio = {}
            WHERE       cliente_id = {}
        """.format(self.denominacion, self.nif, self.domicilio.domicilio_id)
        DBQuery(db_data).execute(sql)


class ClienteView(object):
    
    def agregar(self):
        with open("{}/cliente_agregar.html".format(STATIC_PATH), "r") as f:
	    form = f.read()

	regex = "<!-- errores -->(.|\n)+<!-- errores -->"
	form = sub(regex, '', form)

	print HTTP_HTML
	print ""
	print Template(TEMPLATE_PATH).render_inner(form)
    
    def ver(self, cliente):
        with open("{}/cliente_ver.html".format(STATIC_PATH), "r") as f:
	    ficha = f.read()

        diccionario = vars(cliente)
        diccionario.update(vars(cliente.domicilio))
        ficha = Template(base=ficha).render(diccionario)

        print HTTP_HTML
        print ""
        print Template(TEMPLATE_PATH).render_inner(ficha)

    def editar(self, cliente):
	with open("{}/cliente_editar.html".format(STATIC_PATH), "r") as f:
	    form = f.read()

	regex = "<!-- errores -->(.|\n)+<!-- errores -->"
	ficha = sub(regex, '', form)

        diccionario = vars(cliente)
        diccionario.update(vars(cliente.domicilio))
        ficha = Template(base=ficha).render(diccionario)

        print HTTP_HTML
        print ""
        print Template(TEMPLATE_PATH).render_inner(ficha)

    def listar(self, coleccion):
	pila = []
	tabla = Template('{}/cliente_listar.html'.format(STATIC_PATH)).get_template()
	fila = Template(base=tabla).extract('fila')

	for cliente in coleccion:
	    diccionario = vars(cliente)
            diccionario.update(vars(cliente.domicilio))
	    render = Template(base=fila).render(diccionario)
	    pila.append(render)

	pila = ''.join(pila)

	contenido = tabla.replace(fila, pila)

	print HTTP_HTML
	print ""       
	print Template(TEMPLATE_PATH).render_inner(contenido)


class ClienteController(object):

    def __init__(self):
        self.model = Cliente()
        self.view = ClienteView()

    def agregar(self):
        self.view.agregar()

    def guardar(self):
        formulario = FieldStorage()

        self.model.domicilio.calle = formulario['calle'].value
        self.model.domicilio.numero = formulario['numero'].value
        self.model.domicilio.planta = formulario['planta'].value
        self.model.domicilio.puerta = formulario['puerta'].value
        self.model.domicilio.ciudad = formulario['ciudad'].value
        self.model.domicilio.insert()
        
        self.model.denominacion = formulario['denominacion'].value
        self.model.nif = formulario['nif'].value
        self.model.insert()

        print HTTP_HTML
        print "Location: {}/cliente/ver/{}".format(HOST, self.model.cliente_id)
        print ""
        print ""

    def ver(self):
        self.model.cliente_id = ARG 
        self.model.select()

        self.view.ver(self.model)

    def editar(self):
        self.model.cliente_id = ARG
        self.model.select()
        
        self.view.editar(self.model)

    def actualizar(self):
        formulario = FieldStorage()
        self.model.cliente_id = formulario['cliente_id'].value
        self.model.nif = formulario['nif'].value
        self.model.domicilio.domicilio_id = self.model.domicilio
        self.model.domicilio.calle = formulario['calle'].value
        self.model.domicilio.numero = formulario['numero'].value
        self.model.domicilio.planta = formulario['planta'].value
        self.model.domicilio.puerta = formulario['puerta'].value
        self.model.domicilio.ciudad = formulario['ciudad'].value
        self.model.domicilio.update()
        self.model.update()
        
        print HTTP_HTML
        print "Location: {}/cliente/ver/{}".format(HOST, self.model.cliente_id)
        print ""
        print ""

    def eliminar(self):
        self.model.cliente_id = ARG
        self.model.delete()
        
        print HTTP_HTML
        print "Location: {}/cliente/listar".format(HOST)
        print ""
        print ""

    def listar(self):
	c = Collector()
        c.get("Cliente")
	self.view.listar(c.coleccion)