from core.db import DBQuery
from settings import db_data, HTTP_HTML


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
    pass

class DatoDeContactoController(object):
    
    def __init__(self):
        self.model = DatoDeContacto()
        self.view = DatoDeContactoView()

    def guardar(self, formulario, cliente_id):
        # Condicional ternario
        
        self.model.cliente = cliente_id
       
        self.model.denominacion = "Teléfono"
        self.model.valor = formulario['telefono'].value
        self.model.insert() 

        self.model.denominacion = "Móvil"
        self.model.valor = formulario['movil'].value
        self.model.insert() 

        self.model.denominacion = "Email"
        self.model.valor = formulario['email'].value
        self.model.insert() 
