from twisted.web.iweb import IRenderable
from twisted.python.components import registerAdapter
from zope.interface import implements
from jinja2 import Environment, PackageLoader, FileSystemLoader

env = Environment(loader=FileSystemLoader('templates'))


