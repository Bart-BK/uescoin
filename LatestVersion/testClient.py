import socket
import uuid
import time
import genesis
import pickle

"""
	Enviando uma transacao
"""
objOut = pickle.dumps(('transaction', uuid.uuid4().int, time.time(), 10, 0, 1, 0)) #Serializando
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp.connect(('127.0.0.1', 5555))
tcp.send(objOut)
objIn = pickle.loads(tcp.recv(4096))
print(objIn)