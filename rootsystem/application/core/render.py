# -*- coding: utf-8 -*-
from re import search
from string import Template as PyTemplate

from config import author_data


class Template:

    def __init__(self, path='', base=''):
        self.path = path
        self.template = base if base else self.get_template()

    def get_template(self):
        with open(self.path, 'r') as t:
            return t.read()

    def render(self, values):
        values.update(author_data)
        return PyTemplate(self.template).safe_substitute(values) 

    def render_inner(self, inner):
        values = dict(content=inner)
        values.update(author_data)
        render = PyTemplate(self.template).safe_substitute(values)
        return render

    def extract(self, tag):
        regex = "<!--{t}-->(.|\n)+<!--{t}-->".format(t=tag)
	code = search(regex, self.template).group(0)
        return code
