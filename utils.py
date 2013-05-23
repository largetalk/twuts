import hashlib
import string
from cStringIO import StringIO
from settings import SALT_KEY
from twisted.web.client import getPage, Agent
from twisted.internet import reactor
from twisted.web.http_headers import Headers
from twisted.internet import defer
from twisted.web.client import FileBodyProducer
import json
from twisted.internet.protocol import Protocol
from twisted.python import log

def short_url(long_url):
    array = string.ascii_letters + string.digits
    md5 = hashlib.md5().update(SALT_KEY + long_url).hexdigest()
    short_url_lst = []
    for i in range(4):
        part_str = ''
        part = int(md5[i*8 : i*8 + 8], 16) & 0x3FFFFFFF
        for j in range(6):
            part_str += array[part & 0x0000001F]
            part = part >> 5
        short_url_lst.append(part_str)
    return short_url_lst

class JsonParse(Protocol):
    def __init__(self, finished):
        self.finished = finished
        self.js_data = None

    def dataReceived(self, bytes):
        self.js_data = json.loads(bytes)

    def connectionLost(self, reason):
        log.msg('Finised received body: %s' % reason.getErrorMessage())
        self.finished.callback(self.js_data)


agent = Agent(reactor)

def get_google_short_url(long_url):
    body = FileBodyProducer(StringIO(json.dumps({'longUrl': long_url})))
    d = agent.request(
            'POST',
            'https://www.googleapis.com/urlshortener/v1/url',
            Headers({'Content-Type': ['application/json']}),
            body)
    
    def handle_response(response):
        if response.code == 200:
            finished = defer.Deferred()
            response.deliverBody(JsonParse(finished))
        else:
            finished = defer.succeed({'id':'failed'})
        return finished
        
    d.addCallback(handle_response)
    return d

def get_google_long_url(short_url):
    url = 'https://www.googleapis.com/urlshortener/v1/url?shortUrl=%s' % short_url
    d = agent.request(
            'GET',
            url,
            Headers({'Content-Type': ['application/json']}),
            None)

    def handle_response(response):
        if response.code == 200:
            finished = defer.Deferred()
            response.deliverBody(JsonParse(finished))
        else:
            finished = defer.succeed({'id':'failed', 'status': 'Failed', 'longUrl':'Failed'})
        return finished

    d.addCallback(handle_response)
    return d



