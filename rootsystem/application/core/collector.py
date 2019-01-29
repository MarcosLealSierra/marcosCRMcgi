from core.db import DBQuery
from settings import db_data, MODULE, PACKAGE


class Collector(object): 

    def __init__(self):
        self.coleccion = []

    def get(self, clase):
        sql = "SELECT {c}_id FROM {c}".format(c=str(clase))
        pids = DBQuery(db_data).execute(sql)
        
        modulo = __import__(PACKAGE, fromlist=[MODULE])
        
        for pid in pids:
            modelo = getattr(modulo, MODULE.title())()
            vars(modelo)["{}_id".format(MODULE)] = pid[0]
            modelo.select()
            self.coleccion.append(modelo)
