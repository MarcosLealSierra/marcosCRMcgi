from core.db import DBQuery
from settings import db_data


class StdObject(object):

    def delete(self, propiedad_id):
        clase = self.__class__.__name__

        sql = "DELETE FROM {c} WHERE {c}_id = {pi}".format(
            c = clase.lower(), pi = propiedad_id)
        DBQuery(db_data).execute(sql)
