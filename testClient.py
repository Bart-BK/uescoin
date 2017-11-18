import socket
import uuid
import time
import genesis
import pickle

obj = pickle.dumps(['transaction', uuid.uuid4().int, time.time(), 10, 0, 1, 0])
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp.connect(('127.0.0.1', 5555))
tcp.send(obj)
print(tcp.recv(4096).decode('UTF-8'))