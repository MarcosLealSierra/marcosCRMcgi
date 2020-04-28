from core.db import DBQuery
from core.stdobject import StdObject
from settings import db_data


class Domicilio(StdObject):

    def __init__(self):
        self.domicilio_id = 0
        self.calle = ''
        self.numero = ''
        self.planta = 0
        self.puerta = ''
        self.ciudad = ''

    def insert(self):
        sql = """
            insert into     domicilio
                            (calle, numero, planta, puerta, ciudad)
            values          ('{}', '{}', {}, '{}', '{}')
        """.format(
            self.calle,
            self.numero,
            self.planta,
            self.puerta,
            self.ciudad
        )
        self.domicilio_id = DBQuery(db_data).execute(sql)

    def update(self):
        sql = """
            UPDATE      domicilio
            SET         calle = '{}', numero = '{}', planta = {}, puerta = '{}', ciudad = '{}'
            WHERE       domicilio_id = {}
        """.format(
            self.calle,
            self.numero,
            self.planta,
            self.puerta,
            self.ciudad,
            self.domicilio_id
        )
        DBQuery(db_data).execute(sql)
