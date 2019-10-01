class ControllerFactory(object):

    def make(cls, cls_name):
        clslower = cls_name.replace("Controller", "").lower()
        module = __import__("modules.{}".format(clslower), fromlist=[cls_name])
        obj = getattr(module, cls_name)()
        return obj
