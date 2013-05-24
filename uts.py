from urllib2 import urlparse
from klein import run, route
from klein.app import _globalKleinApp
from twisted.internet import defer
from utils import get_google_short_url, get_google_long_url
from template import env as jinja_env

from db import duan

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



@route('/url/', methods=['GET', 'POST'])
def entry_login(request):
    if request.method == 'GET':
        short_url = request.args.get('shortUrl', [None])[0]
        if not short_url:
            return 'require shortUrl'
        pr = urlparse.urlparse(short_url)
        path = pr.path.strip('/')
        path = path[ path.rfind('/') + 1 : ]

        return duan.get_long_url(path)
    if request.method == 'POST':
        long_url = request.args.get('longUrl', [None])[0]
        if not long_url:
            return 'require longUrl'
        return duan.insert_long_url(long_url)

    return 'Undefine method'



run('localhost', 8080, keyFile='private.pem', certFile='cacert.pem')
