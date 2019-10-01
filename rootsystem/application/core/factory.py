class Factory(object):
   
    def _get(cls, obj, objid):
        setattr(obj, "{}_id".format(clslower), objid)
        obj.select()
        return obj

    def make(cls, cls_name, objid=0):
        clslower = cls_name.lower()
        module = __import__("modules.{}".format(clslower), fromlist=[cls_name])
        obj = getattr(module, cls_name)()
        if objid: cls._get(obj, objid)
        return obj
