from core.db import DBQuery
from core.helpers import compose
from settings import db_data


class LogicalConnector(object):
    
    _clase_compuesto = ''           
    _propiedad_id_compuesto = ''   
    _compositor = ''                
    _propiedad_id_compositor = ''   
    
    def __init__(self, compuesto, compositor):
        self._set_variables(compuesto, compositor)

        self.compositorcompuesto_id = 0
        self.compuesto = compuesto
        self.compositor = self._get_collection(compositor)
        self.fm = 0

    def _set_variables(self, compuesto, compositor):
        self._clase_compuesto = compuesto.__class__.__name__.lower()
        self._propiedad_id_compuesto = '{}_id'.format(self._clase_compuesto)
        self._compositor = compositor.lower()
        self._propiedad_id_compositor = '{}_id'.format(self._compositor)

    def _get_collection(self, compositor):
        compuesto_collection = '{}_collection'.format(compositor.lower())
        return self.compuesto.__dict__[compuesto_collection]

    def delete(self):
        sql = """DELETE FROM  {compositor}{compuesto} 
                 WHERE        compuesto = {pi}""".format(
            compositor=self._compositor,
            compuesto=self._clase_compuesto,
            pi=self.compuesto.__dict__[self._propiedad_id_compuesto]
        )
        DBQuery(db_data).execute(sql)

    def insert(self):
        self.delete()
        sql = """
            INSERT INTO {compositor}{compuesto}
            (compuesto, compositor, fm)
            VALUES """.format(
                compositor=self._compositor,
                compuesto=self._clase_compuesto
            )

        tuplas = []
        for compositor in self.compositor:
            tupla = "({}, {}, {})".format(
                self.compuesto.__dict__[self._propiedad_id_compuesto],
                compositor.__dict__[self._propiedad_id_compositor],
                compositor.fm
            )
            tuplas.append(tupla)

        sql = "{}{}".format(sql, ", ".join(tuplas))
        DBQuery(db_data).execute(sql)

    def select(self):
        sql = """
            SELECT  compositor, fm
            FROM    {compositor}{compuesto}
            WHERE   compuesto = {pi}
        """.format(
                compositor=self._compositor,
                compuesto=self._clase_compuesto,
                pi=self.compuesto.__dict__[self._propiedad_id_compuesto]
            )
        resultados = DBQuery(db_data).execute(sql)
        
        modulo = __import__(
            'modules.{}'.format(self._compositor),
            fromlist=[self._compositor.capitalize()]
        )

        for resultado in resultados:
            obj_compositor = getattr(modulo, self._compositor.capitalize())()
            setattr(obj_compositor, self._propiedad_id_compositor, resultado[0])
            obj_compositor.select()
            colectora = '{}_collection'.format(self._compositor)
            self.compuesto.__dict__[colectora].append(obj_compositor)
            obj_compositor.fm = resultado[1]
