from os.path import isfile

from core.db import DBQuery
from core.helpers import get_form_value, get_hash, redirect
from core.render import Template
from core.sessions import Sessions
from settings import CREDENTIAL_PATH, db_data, HTTP_HTML, STATIC_PATH, \
    TEMPLATE_PATH

from re import sub


class User(object):

    def __init__(self):
        self.user_id = ''
        self.denomination = ''
        self.level = 0

    def insert(self):
        sql = """
        INSERT INTO user
                    (user_id, denomination, level)
        VALUES      ('{}', '{}', {})
        """.format(
            self.user_id, 
            self.denomination, 
            self.level
        )

        DBQuery(db_data).execute(sql)

    def select(self):
        sql = """
        SELECT  denomination, level
        FROM    user
        WHERE   user_id = '{}'
        """.format(self.user_id)
        
        resultados = DBQuery(db_data).execute(sql)[0]
        self.denomination = resultados[0]
        self.level = resultados[1]


class UserView(object):

    def agregar(self, errors=[], fields={}): #form?
        errors = "<br>".join(errors)
        with open("{}/user_agregar.html".format(STATIC_PATH), "r") as f:
            form = f.read()
        
        dictionary = dict()
        dictionary['errors'] = errors
        dictionary['denomination'] = get_form_value("denomination")
        dictionary['level'] = get_form_value("level")
        
        if not errors:
            regex = "<!-- errores -->(.|\n)+<!-- errores -->"
            form = sub(regex, '', form)
        
        form = Template(base=form).render(dictionary)
        
        print(HTTP_HTML, "\n")
        print(Template(TEMPLATE_PATH).render_inner(form))

    def login(self):
        fichero = "{}/user_login".format(STATIC_PATH)
        formulario = Template(fichero).get_template()
        print(HTTP_HTML, "\n")
        print(Template(TEMPLATE_PATH).render_inner(formulario))


class UserController(object):
    
    def __init__(self):
        self.model = User()
        self.view = UserView()

    def agregar(self):
        self.view.agregar()

    def guardar(self):
        user_hash = get_hash("sha256", get_form_value("username"))
        pass_hash = get_hash("sha512", get_form_value("password"))
        user_id = get_hash("sha384", get_form_value("username"))
        user_id = get_hash("md5", user_id)
        denomination = get_form_value("denomination")
        level = int(get_form_value("level"))

        salt_username = get_form_value("username")[0:2]
        salt_password = get_form_value("password")[1:]
        salt = get_hash("sha224", "{}{}".format(salt_username, salt_password))
        credential = get_hash("sha1", "{}{}{}".format(salt, user_hash, pass_hash))
        filename = "{}/.{}".format(CREDENTIAL_PATH, credential)

        with open(filename, "w") as f:
            f.write("")

        self.model.user_id = user_id
        self.model.denomination = denomination
        self.model.level = level
        self.model.insert()

        Template.print(vars(self.model))

    def login(self):
        Sessions.start()
        self.view.login()

    def validar(self):
        user_hash = get_hash("sha256", get_form_value("username"))
        pass_hash = get_hash("sha512", get_form_value("password"))
        user_id = get_hash("sha384", get_form_value("username"))
        user_id = get_hash("md5", user_id)
        salt_username = get_form_value("username")[0:2]
        salt_password = get_form_value("password")[1:]
        salt = get_hash("sha224", "{}{}".format(salt_username, salt_password))
        credential = get_hash("sha1", "{}{}{}".format(salt, user_hash, pass_hash))
        filename = "{}/.{}".format(CREDENTIAL_PATH, credential)

        if isfile(filename):
            #sesiónnnnn
        else:
            redirect("/user/login")

    def logout(self):
        # TODO destruir sesión
        redirect("/user/login")
