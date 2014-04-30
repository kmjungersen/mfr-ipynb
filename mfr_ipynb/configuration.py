# -*- coding: utf-8 -*-
"""Configuration object for the mfr-ipynb module."""

import os
import inspect
from mako.lookup import TemplateLookup

from IPython.config import Config
from IPython.nbconvert.exporters import HTMLExporter


class ipynb_config(object):

    STATIC_PATH = '/static'

    def __init__(cls):
        class_file = inspect.getfile(cls)
        cls.path = os.path.split(class_file)[0]
        cls.mako_lookup = TemplateLookup(
            directories=[os.path.join(cls.path, 'templates')]
        )

    def exporter(self):
        c = Config()
        c.HTMLExporter.template_file = 'basic'
        c.NbconvertApp.fileext = 'html'
        c.CSSHTMLHeaderTransformer.enabled = False
        c.Exporter.filters = {'strip_files_prefix': lambda s: s}
            #don't strip the files prefix
        exporter = HTMLExporter(config=c)
        return exporter

    def render_mako(cls, filename, **kwargs):
        return cls.mako_lookup.get_template(filename).render(**kwargs)

