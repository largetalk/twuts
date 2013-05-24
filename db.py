import txmongo
import txmongo.filter
from settings import MONGODB, SALT_KEY
from twisted.internet import defer
import json
import hashlib
from utils import short_url as gen_short_url

connection = txmongo.lazyMongoConnection(MONGODB['HOST'], MONGODB['PORT'])
db = connection[MONGODB['NAME']]


class ShortUrlDoc(object):
    def get_long_url(self, short_url):
        fields = {'lurl': 1}
        d = db.url.find({'surl': short_url}, limit=1, fields=fields)

        def _cb(docs):
            if docs:
                return docs[0]['lurl']
            else:
                return 'no record\n'

        d.addCallback(_cb)
        return d

    def insert_long_url(self, long_url):
        m = hashlib.md5()
        m.update(SALT_KEY + long_url)
        md5 = m.hexdigest()
        d = db.url.find({'hash': md5})

        def _cb(docs):
            if docs:
                return json.dumps({'status': 'OK', 'shortUrl': docs[0]['surl']})
            else:
                short_url = gen_short_url(long_url)[0]
                finished = db.url.insert({
                    'surl': short_url,
                    'lurl': long_url,
                    'hash': md5}, safe=True)

                def _innercb(result):
                    return json.dumps({'status': 'OK', 'shortUrl': short_url})

                finished.addCallback(_innercb)
                return finished

        d.addCallback(_cb)
        return d


duan = ShortUrlDoc()
