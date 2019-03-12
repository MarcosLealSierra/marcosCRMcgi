from core.db import DBQuery
from settings import db_data


class StdObject(object):

    def delete(self):
        clase = self.__class__.__name__
        sql = "DELETE FROM {c} WHERE {c}_id = {pi}".format(c = clase.lower(), 
            pi = self.__dict__['{}_id'.format(clase.lower())])
        DBQuery(db_data).execute(sql)
