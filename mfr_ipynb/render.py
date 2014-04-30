"""ipynb render module"""

import re
import os.path

from IPython.nbformat import current as nbformat
import inspect
import os
from mako.template import Template
from mfr import config as core_config
from IPython.config import Config as IPythonConfig
from IPython.nbconvert.exporters import HTMLExporter


def render_html(fp, *args, **kwargs):
    content = fp.read()
    nb = parse_json(content)
    name, theme = get_metadata(nb)
    exporter = get_ipython_exporter()
    body = exporter.from_notebook_node(nb)[0]

    return render_mako(
        "templates/ipynb.mako", filename=name, css_theme=theme, mathjax_conf=None,
        body=body, STATIC_PATH=core_config["STATIC_PATH"]
    )

def parse_json(content):
    try:
        nb = nbformat.reads_json(content)
    except ValueError:
        raise NbFormatError('Error reading json notebook')
    return nb

def get_metadata(nb):
    # notebook title
    name = nb.get('metadata', {}).get('name', None)
    if not name:
        name = "untitled.ipynb"
    if not name.endswith(".ipynb"):
        name += ".ipynb"

    # css
    css_theme = nb.get('metadata', {})\
                  .get('_nbviewer', {})\
                  .get('css', None)
    if css_theme and not re.match('\w', css_theme):
        css_theme = None
    return name, css_theme

def NbFormatError(Exception):
    pass

def get_ipython_exporter():
    c = IPythonConfig()
    c.HTMLExporter.template_file = 'basic'
    c.NbconvertApp.fileext = 'html'
    c.CSSHTMLHeaderTransformer.enabled = False
    c.Exporter.filters = {'strip_files_prefix': lambda s: s}
        #don't strip the files prefix
    exporter = HTMLExporter(config=c)
    return exporter

def render_mako(tmp_filename, **kwargs):
    return Template(tmp_filename).render(**kwargs)
