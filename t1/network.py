import pickle
import socket
from threading import Thread

class ServerListener:
	def __init__(self, dispatcherClass):
		if dispatcherClass is None or not issubclass(dispatcherClass, Dispatcher):
			raise ValueError('Argument should be Dispatcher type')

		self.dispatcherClass = dispatcherClass
		self.serverSocket = None
		self.clients = []

	def start(self, host = '127.0.0.1', port = 45678, queueSize = 5):
		try:
			self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.serverSocket.bind((host, port))
			self.serverSocket.listen(queueSize)
			
			print('Server started on %s:%d\n' % (host, port))

			while True:
				clientSocket = self.serverSocket.accept()
				Thread(target = self.forward, args = (clientSocket,)).start()
		except OSError as e:
			self.serverSocket.close()
			print('Server closed: ', e)

	def stop(self):
		self.serverSocket.close()
		print('Server stopped')

	def dump(self):
		dumped = self.clients
		self.clients = None
		return dumped

	def removeClient(self, clientSocket):
		self.clients.remove(clientSocket)

	def forward(self, conn):
		conn, addr = conn
		print('\nConnection established with %s:%d\n' % addr)
		self.clients.append(conn)
		self.dispatcherClass().incoming(conn, self)

class Dispatcher:
	def __del__(self):
		self.close()

	def incoming(self, conn, listener):
		self.listener = listener
		self.requester = Protocol(conn)
		self.execute(self.requester.receiveParams())

	def execute(self, params):
		try:
			returnValue = getattr(self, params[0])(*params[1:])
		except (TypeError, AttributeError) as e:
			print('Protocol error. %s: %s\n' % (type(e).__name__, e))

	def before(self, params):
		pass

	def after(self):
		pass

	def close(self):
		self.requester.close()
		self.listener.removeClient(self.requester.conn)

class Protocol:
	def __init__(self, connection):
		if type(connection) == socket.socket:
			self.conn = connection
		else:
			self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.conn.connect(connection)

	def sendParams(self, *protocol):
		self.conn.send(pickle.dumps(protocol))

	def receiveParams(self, bufSize = 4096):
		return pickle.loads(self.conn.recv(bufSize))

	def close(self):
		self.conn.close()