from globl import *
from network import Protocol
import time
import uuid

proto = Protocol((NET_LOCAL['HOST'], NET_LOCAL['PORT']))
proto.sendParams('chaining', ('transaction', uuid.uuid4().int, time.time(), 1000, 3, 1, 3))
proto.close()
