from modules.cliente import Cliente


class ClienteHelper(object):

    @staticmethod
    def get_name(idc=0):
        c = Cliente()
        c.cliente_id = idc
        c.select()
        return c.denominacion
