def compose(obj, cls):
    if isinstance(obj, cls) or obj is None:
        return obj
    else:
        raise TypeError('{} no es de tipo {}'.format(type(obj), cls))
