"""ipynb render module"""

import re
import os.path
from IPython.config import Config
    #from IPython.nbconvert import export_python
from IPython.nbconvert.exporters import TemplateExporter
from IPython.nbformat import current as nbformat
from IPython.nbconvert.exporters import HTMLExporter
from mako.lookup import TemplateLookup
from configuration import ipynb_config

def render_html(fp, *args, **kwargs):
    content = fp.read()
    nb = parse_json(content)
    name, theme = get_metadata(nb)
    exporter = ipynb_config.exporter()
    body = exporter.from_notebook_node(nb)[0]

    return ipynb_config.render_mako(
        "ipynb.mako", file_name=name, css_theme=theme, mathjax_conf=None,
        body=body, STATIC_PATH=ipynb_config.STATIC_PATH
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