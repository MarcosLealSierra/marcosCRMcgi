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
