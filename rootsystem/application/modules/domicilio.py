from core.db import DBQuery
from settings import db_data


class Domicilio(object):   # compositor: compone a...

    def __init__(self):
        self.domicilio_id = 0
        self.calle = ''
        self.numero = ''
        self.planta = 0
        self.puerta = ''
        self.ciudad = ''

    def insert(self):
        sql = """
            INSERT INTO     domicilio
                            (calle, numero, planta, puerta, ciudad)
            VALUES          ('{}', '{}', {}, '{}', '{}')
        """.format(self.calle, self.numero, self.planta, self.puerta, 
            self.ciudad)
        self.domicilio_id = DBQuery(db_data).execute(sql)
  
    def select(self):
        sql = """
            SELECT      calle, numero, planta, puerta, ciudad
            FROM        domicilio
            WHERE       domicilio_id = {}
        """.format(self.domicilio_id)
        resultados = DBQuery(db_data).execute(sql)[0]
        self.calle = resultados[0]
        self.numero = resultados[1]
        self.planta = resultados[2]
        self.puerta = resultados[3]
        self.ciudad = resultados[4]
    
    def update(self):
        sql = """
            UPDATE      domicilio
            SET         calle = '{}', numero = '{}', planta = {}, 
                        puerta = '{}', ciudad = '{}'
            WHERE       domicilio_id = {}
        """.format(self.calle, self.numero, self.planta, self.puerta,
            self.ciudad)
        DBQuery(db_data).execute(sql)
