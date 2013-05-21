import txmongo
from settings import MONGODB
from twisted.internet import defer

connection = txmongo.lazyMongoConnection(MONGODB['HOST'], MONGODB['PORT'])
db = connection[MONGODB['NAME']]

def get_entrys():
    def callback(r):
        return str(r)

    d = db.entry.find(limit=10)
    d.addCallback(callback)
    return d
