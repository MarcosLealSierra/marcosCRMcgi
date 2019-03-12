from core.db import DBQuery
from settings import db_data


class StdObject(object):

    def delete(self):
        clase = self.__class__.__name__.lower()
        propiedad_id = '{}_id'.format(clase)

        sql = "DELETE FROM {c} WHERE {c}_id = {pi}".format(c=clase, 
            pi=self.__dict__[propiedad_id])
        DBQuery(db_data).execute(sql)

