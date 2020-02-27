from core.db import DBQuery
from core.logicalconnector import LogicalConnector
from settings import HTTP_HTML, db_data


class StdObject(object):

    #def insert(self):
        #clase = self.__class__.__name__.lower()
        #propiedades = vars(self).keys()
        #valores = vars(self).values()
        #lista_valores = list(valores)
        #for i, v in enumerate(lista_valores):
            #if isinstance(v, str):
                #lista_valores[i] = "'{}'".format(v)
            #elif isinstance(v, int):
                #pass
            #else:
                #lista_valores[i] = str(v)

        #sql = """
            #INSERT INTO     {c} 
                            #({p})
            #VALUES          ({v})
        #""".format(
                #c=clase,
                #p=", ".join(propiedades),
                #v=", ".join(lista_valores)
            #)

        #self.__dict__['{}_id'.format(clase)] = DBQuery(db_data).execute(sql)

    def select(self):
        clase = self.__class__.__name__.lower()
        propiedad_id = '{}_id'.format(clase)

        propiedades = vars(self)

        campos_tabla = []
        for campo in propiedades:
            if not isinstance(propiedades[campo], list):
                campos_tabla.append(campo)

        sql = "SELECT {cp} FROM {c} WHERE {c}_id = {pi}".format(
            cp=", ".join(campos_tabla),
            c=clase,
            pi=self.__dict__[propiedad_id]
        )
        resultados = DBQuery(db_data).execute(sql)[0]

        for i, p in enumerate(propiedades.keys()):
            compositor = "{}".format(p.capitalize())
            compositor_id = '{}_id'.format(p)
            archivo = "modules.{}".format(p)

            if self.__dict__[p] is None:
                modulo = __import__(archivo, fromlist=[compositor])
                self.__dict__[p] = getattr(modulo, compositor)()# FACTORY?
                self.__dict__[p].__dict__[compositor_id] = resultados[i]
                self.__dict__[p].select()
            elif isinstance(self.__dict__[p], list):
                pass
                # identificar dependientes e independientes y construirlas
                # según el conector lógico o el get auxiliar
            else:
                self.__dict__[p] = resultados[i]

    #def update(self):
        #clase = self.__class__.__name__.lower()
        #propiedad_id = "{}_id".format(clase)
        #propiedades = vars(self).keys()
        #valores = vars(self).values()
        #elementos_query = list()
        #for i, v in enumerate(valores):
            #if isinstance(v, str):
                #elementos_query.append("{} = '{}'".format(propiedades[i], v))
            #else:
                #elementos_query.append("{} = {}".format(propiedades[i], v))

        #sql = """
            #UPDATE      {c}
            #SET         {e}
            #WHERE       {c}_id = {pi}
        #""".format(
            #c=clase,
            #e=", ".join(elementos_query),
            #pi=self.__dict__[propiedad_id]
        #)

        #print(HTTP_HTML, "\n")
        #print(sql, "<br><br>")
        #DBQuery(db_data).execute(sql)

    def delete(self):
        clase = self.__class__.__name__.lower()
        propiedad_id = '{}_id'.format(clase)

        sql = "DELETE FROM {c} WHERE {c}_id = {pi}".format(
            c=clase,
            pi=self.__dict__[propiedad_id]
        )
        DBQuery(db_data).execute(sql)
