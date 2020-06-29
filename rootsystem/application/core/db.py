import MySQLdb
from settings import DB_HOST, DB_NAME, DB_PASS, DB_USER


class DBQuery(object):

   def __init__(self, data=[]):
       _data = [DB_HOST, DB_NAME, DB_PASS, DB_USER]
       self.data = data if data else _data

   def execute(self, sql):
       self.sql = sql
       conn = MySQLdb.connect(*self.data)
       cursor = conn.cursor()
       cursor.execute(self.sql)
       data = True

       if self.limpiar_sql().upper().startswith('SELECT'):
           data = cursor.fetchall()
       else:
           conn.commit()
           if self.limpiar_sql().upper().startswith('INSERT'):
               data = cursor.lastrowid

       cursor.close()
       conn.close()
       return data

   def limpiar_sql(self):
       return self.sql.replace(' ', '').replace('\n', '')
