from klein import run, route
from klein.app import _globalKleinApp
from twisted.internet import defer
from utils import get_google_short_url, get_google_long_url
from template import env as jinja_env

@route('/')
def root(request):
    #def callback(js_data):
    #    print js_data
    #    return js_data['id']

    #d = get_google_short_url('http://www.google.com')
    #d.addCallback(callback)
    #return d

    @defer.inlineCallbacks
    def callback():
        js_data = yield get_google_short_url('http://www.google.com')
        js_data2 = yield get_google_long_url('http://goo.gl/fbsS')
        content = jinja_env.get_template('base.html').render(short_url=js_data['id'], long_url=js_data2['longUrl'])
        #content = '''
        #<html><body>%s<br>%s</body></html>
        #''' % (js_data['id'], js_data2['longUrl'])
        defer.returnValue(content)
    return callback()



@route('/entry/login/')
def entry_login(request):
    name = request.args.get('name', ['world'])[0]
    return 'login success'


run('localhost', 8080, keyFile='private.pem', certFile='cacert.pem')
