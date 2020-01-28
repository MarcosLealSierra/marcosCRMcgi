#-*- coding: utf-8 -*-
from hashlib import new
from settings import HOST, HTTP_HTML, POST
from sys import version_info as version


class Sanitizer(object):

    @staticmethod
    def purge_alnum(string):
        chars = []
        for c in string:
            if c.isalnum(): chars.append(c)
        return "".join(chars)

    @staticmethod
    def convert_to_int(string):
        try:
            string = int(string)
        except:
            string = 0
        finally:
            return string

    @staticmethod
    def get_chars_table():
        valid_chars = [32]
        valid_chars.extend(range(48, 58))   # Números
        valid_chars.extend(range(65, 91))   # Letras mayúsculas
        valid_chars.extend(range(97, 123))  # Letras minúsculas
        valid_chars.extend([
            192, 193, 199, 200, 201, 209, 210, 211, 217, 218, 
            220, 224, 225, 232, 231, 233, 236, 237, 241, 242, 243, 249, 250, 
            252
        ])
        return valid_chars
    
    @staticmethod
    def clean_string(string):
        if version.major == 2: street = unicode(street, encoding="utf-8")
        valid_chars = Sanitizer.get_chars_table()
        valid_chars.extend([39, 46, 170, 186])

        cadena = string
        for char in street:
            if not ord(char) in valid_chars:
                cadena.replace(char, '')

    @staticmethod
    def convert_to_html(string):
        valid_chars = Sanitizer.get_chars_table()

        cadena = string
        for char in string:
            if not ord(char) in valid_chars:
                html_entity = "&#{};".format(ord(char))
                cadena.replace(char, html_entity)
        string = "".join(clean_chain)
        return string

    @staticmethod
    def filter_string(string):
        string = Sanitizer.clean_string(string)
        string = Sanitizer.convert_to_html(string)
        return string


def compose(obj, cls):
    if isinstance(obj, cls) or obj is None:
        return obj
    else:
        raise TypeError('{} no es de tipo {}'.format(type(obj), cls))


def redirect(recurso):
    print(HTTP_HTML)
    print("Location: {}/{}\n".format(HOST, recurso))


def get_form_value(key):
    return "" if not key in POST else POST[key].value


def get_hash(algorithm, string):
    if version.major == 2:
        h = new(algorithm, string)
    else:
        h = new(algorithm, bytes(string, encoding="utf8"))

    return h.hexdigest()
