from cgi import FieldStorage
from re import sub

from core.db import DBQuery
from core.helpers import redirect
from core.render import Template
from settings import ARG, db_data, HTTP_HTML, MODULE, STATIC_PATH, TEMPLATE_PATH


class DatoDeContacto(object):

    def __init__(self):
        self.datodecontacto_id = 0
        self.denominacion = ''
        self.valor = ''
        self.cliente = 0
    
    @staticmethod
    def get_datosdecontacto(oid=0):
        sql = "SELECT datodecontacto_id FROM datodecontacto WHERE cliente = {}".format(oid)
        return DBQuery(db_data).execute(sql)
    
    def insert(self):
        sql = """
            INSERT INTO     datodecontacto
                            (denominacion, valor, cliente)
            VALUES          ('{}', '{}', {})
        """.format(
            self.denominacion,
            self.valor,
            self.cliente
        )
        self.datodecontacto_id = DBQuery(db_data).execute(sql)

    def select(self):
        sql = """
            SELECT      denominacion, valor, cliente
            FROM        datodecontacto
            WHERE       datodecontacto_id = {}
        """.format(self.datodecontacto_id)
        resultados = DBQuery(db_data).execute(sql)[0]
        self.denominacion = resultados[0]
        self.valor = resultados[1]
        self.cliente = resultados[2]

    def update(self):
        sql = """
            UDPATE      datodecontacto
            SET         denominacion = '{}', valor = '{}', cliente = {}
            WHERE       datodecontacto_id = {}
        """.format(
            self.denominacion,
            self.valor,
            self.cliente,
            self.datodecontacto_id
        )
        DBQuery(db_data).execute(sql)

    def delete(self):
        sql = "DELETE FROM datodecontacto WHERE datodecontacto_id = {}".format(
            self.datodecontacto_id)
        DBQuery(db_data).execute(sql)


class DatoDeContactoView(object):

    def agregar(self, cliente_id):
        with open("{}/datodecontacto_agregar.html".format(STATIC_PATH), "r") as f:
            form = f.read()

        regex = "<!-- errores -->(.|\n)+<!-- errores -->"
        form = sub(regex, '', form)

        diccionario = dict(cliente=cliente_id)
        contenido = Template(base=form).render(diccionario)

        print(HTTP_HTML, "\n")
        print(Template(TEMPLATE_PATH).render_inner(contenido))


class DatoDeContactoController(object):
    
    def __init__(self):
        self.model = DatoDeContacto()
        self.view = DatoDeContactoView()

    def agregar(self):
        self.model.cliente = int(ARG)
        self.view.agregar(self.model.cliente)

    def guardar(self, formulario={}, cliente_id=0):     
        if not formulario: formulario = FieldStorage()
        if not cliente_id: cliente_id = formulario['cliente'].value
        self.model.cliente = cliente_id

        if formulario['telefono'].value:
            self.model.denominacion = "Teléfono"
            self.model.valor = formulario['telefono'].value
            self.model.insert() 

        self.model.denominacion = "Móvil"
        self.model.valor = formulario['movil'].value
        self.model.insert() 

        self.model.denominacion = "Email"
        self.model.valor = formulario['email'].value
        self.model.insert()

        if MODULE == "datodecontacto":
            redirect("cliente/ver/{}".format(cliente_id))


class Datodecontacto(DatoDeContacto): pass
class DatodecontactoController(DatoDeContactoController): pass
