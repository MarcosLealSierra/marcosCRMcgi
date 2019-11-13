from core.db import DBQuery
from core.helpers import redirect
from core.render import Template
from settings import datos, STATIC_PATH, TEMPLATE_PATH


class Usuario(object):

    def __init__(self):
        self.usuario_id = ''
        self.denominacion = ''
        self.nivel = 0

    def insert(self):
        sql = """
        INSERT INTO usuario
                    (usuario_id, denominacion, nivel)
        VALUES      ('{}', '{}', {})
        """.format(
            self.usuario_id, 
            self.denominacion, 
            self.nivel
        )

        DBQuery(datos).execute(sql)

    def select(self):
        sql = """
        SELECT  denominacion, nivel
        FROM    usuario
        WHERE   usuario_id = '{}'
        """.format(self.usuario_id)
        
        resultados = DBQuery(datos).execute(sql)[0]
        self.denominacion = resultados[0]
        self.nivel = resultados[1]


class UsuarioView(object):

    def agregar(self):
        fichero = '{}/usuario_agregar.html'.format(STATIC_PATH)
        formulario = Template(fichero).get_template()
        print(HTTP_HTML, "\n")
        print(Template(TEMPLATE_PATH).render_inner(formulario))

    def login(self):
        fichero = "{}/usuario_login".format(STATIC_PATH)
        formulario = Template(fichero).get_template()
        print(HTTP_HTML, "\n")
        print(Template(TEMPLATE_PATH).render_inner(formulario))


class UsuarioController(object):
    
    def __init__(self):
        self.model = Usuario()
        self.view = UsuarioView()

    def agregar(self):
        self.view.agregar()

    def guardar(self):
        pass

    def login(self):
        self.view.login()

    def validar(self):
        pass

    def logout(self):
        # TODO destruir sesión
        redirect("/usuario/login")
