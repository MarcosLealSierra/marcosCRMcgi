from core.db import DBQuery
from settings import db_data


class StdObject(object):

    def delete(self):
        clase = self.__class__.__name__
        modulo = __import__("modules.{}".format(clase.lower()), fromlist=[clase])
        modelo = getattr(modulo, clase)()
        propiedad_id = vars(modelo)["{}_id".format(clase.lower())]


        sql = "DELETE FROM {c} WHERE {c}_id = {pi}".format(
            c = clase.lower(), pi = propiedad_id)
        DBQuery(db_data).execute(sql)
