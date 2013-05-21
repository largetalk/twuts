from klein import run, route
from klein.app import _globalKleinApp
from twisted.internet import defer
from db import get_entrys

@route('/')
def root(request):
    return get_entrys()

@route('/entry/login/')
def entry_login(request):
    name = request.args.get('name', ['world'])[0]
    return 'login success'


run('localhost', 8080)
