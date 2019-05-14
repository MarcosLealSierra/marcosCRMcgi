from core.db import DBQuery
from settings import db_data


class StdObject(object):

    def delete(self):
        clase = self.__class__.__name__.lower()
        propiedad_id = '{}_id'.format(clase)

        sql = "DELETE FROM {c} WHERE {c}_id = {pi}".format(
            c=clase, 
            pi=self.__dict__[propiedad_id]
        )
        DBQuery(db_data).execute(sql)

    def select(self):
        clase = self.__class__.__name__.lower()
        propiedad_id = '{}_id'.format(clase)
        
        propiedades = vars(self).keys()

        sql = "SELECT {p} FROM {c} WHERE {c}_id = {pi}".format(
            p=", ".join(propiedades), 
            c=clase, 
            pi=self.__dict__[propiedad_id]
        )
        resultados = DBQuery(db_data).execute(sql)[0]
        
        for i, p in enumerate(propiedades):
            compositor = "{}".format(p.capitalize())
            compositor_id = '{}_id'.format(p)
            archivo = "modules.{}".format(p)

            if self.__dict__[p] is None:
                modulo = __import__(archivo, fromlist=[compositor])
                self.__dict__[p] = getattr(modulo, compositor)()
                self.__dict__[p].__dict__[compositor_id] = resultados[i]  # self.__dict__[p] es un OBJ
                self.__dict__[p].select()
            elif isinstance(self.__dict__[p], list):
                pass
            else:
                self.__dict__[p] = resultados[i]
