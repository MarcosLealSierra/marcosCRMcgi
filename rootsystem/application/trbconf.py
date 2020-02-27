#-*- coding: utf-8 -*-
from os import mkdir, path


# Directorio para almacenar archivos de sesión
TRB_SESS_DIR = "/tmp/pysessions/"
#TRB_SESS_DIR = "/home/mleal/src/proyectos/marcosCRMcgi/private/pysessions"

# Recurso para autenticar al usuario
TRB_LOGIN_PAGE = "/user/login"

# Página que muestra un error de permisos insuficientes
TRB_RESTRICTED_PAGE = "/user/restricted"

# Recurso por defecto al que se envia al usuario
TRB_DEFAULT_RESOURCE = "/cliente/listar"

# Timeout session
TRB_TIMEOUT = 1440

if not path.isdir(TRB_SESS_DIR):
    mkdir(TRB_SESS_DIR)
