class Controller(object):

    def __init__(self):
        self._set_module()
        self._set_model()
        self._set_view()

    def _set_class(self):
        self._class = self.__class__.__name__.replace("Controller", "")

    def _set_module(self):
        self._set_class()
        self._module = "modules.{}".format(self._class.lower())

    def _set_model(self):
        modelo = __import__(self._module, fromlist=[self._class]) 
        self.model = getattr(modelo, self._class)()

    def _set_view(self):
        name = "{}View".format(self._class)
        view = __import__(self._module, fromlist=[name])
        self.view = getattr(view, name)()
