class Factory(object):
    
    def make(cls, cls_name, objid):
        clslower = cls_name.lower()
        module = __import__("modules.{}".format(clslower), fromlist=[cls_name])
        obj = getattr(module, cls_name)()
        setattr(obj, "{}_id".format(clslower), objid)
        obj.select()
        return obj
