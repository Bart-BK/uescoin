from globl import *
from network import Protocol
import time
import uuid

proto = Protocol((NET_LOCAL['HOST'], NET_LOCAL['PORT']))
proto.sendParams('chaining', ('transaction', uuid.uuid4().int, time.time(), 10, 1, 2, 1))
proto.close()
