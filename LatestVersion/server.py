import socket
import pickle
import defs

class Dispatcher:
	def __init__(self, listener):
		self.listener = listener

	def incoming(self, conn):
		self.conn = conn
		params = pickle.loads(conn.recv(4096))
		try:
			getattr(self, params[0])(*params[1:])
		except (TypeError, AttributeError) as e:
			print('Protocol error. %s: %s' % (type(e).__name__, e))
			conn.send('Protocol error'.encode('UTF-8'))

	def dispatch(self, *protocol):
		self.conn.send(pickle.dumps(protocol))
		self.conn.close()
		self.listener.removeClient(self.conn)

class ServerListener:
	def __init__(self, dispatcher):
		self.dispatcher = dispatcher
		self.server = None
		self.clients = []

	def start(self, HOST = defs.HOST, port = defs.PORT, queueSize = defs.QUEUE_SIZE):
		try:
			self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.server.bind((HOST, port))
			self.server.listen(queueSize)
			print('Server started on %s:%d' % (HOST, port))
			while True:
				client = self.server.accept()
				self.foward(client)
		except OSError as e:
			self.server.close()
			print('Server closed: ', e)

	def stop(self):
		self.server.close()

	def dump(self):
		dumped = self.clients
		self.clients = None
		return dumped

	def removeClient(self, client):
		self.clients.remove(client)

	def foward(self, conn):
		conn, addr = conn
		self.clients.append(conn)
		self.dispatcher(self).incoming(conn)
		print('Connection established with %s:%d' % addr)