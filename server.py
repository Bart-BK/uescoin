import socket
import defs
import pickle
from transaction import Peer
from transaction import Transaction

class Dispatcher:
	def incoming(self, conn):
		self.conn = conn
		params = pickle.loads(conn.recv(4096))		
		try:
			getattr(self, params[0])(*params[1:])
		except (TypeError, AttributeError) as e:
			print('Protocol error. %s: %s' % (type(e).__name__, e))
			conn.send('Protocol error'.encode('UTF-8'))

	def transaction(self, tId, time, value, giverId, receiverId, privateKey):
		print('Incoming transaction: id', tId)
		giver = Peer.find(defs.TX_COMMIT, giverId)
		transfer = giver.balance - value
		if (self.checkPeerId(giver, privateKey) and transfer >= 0):
			receiver = Peer.find(defs.TX_COMMIT, receiverId)
			receiver.balance += transfer
			giver.balance -= transfer
			tx = Transaction()
			tx.id = tId
			tx.time = time
			tx.value = value
			tx.giver = giver
			tx.receiver = receiver
			Transaction.save(defs.TX_TEMP, tx)
			ackStatus = True
		else:
			ackStatus = False
		self.ack(tId, defs.WHO_I_AM, ackStatus)

	def checkPeerId(self, peer, privateKey):
		if peer.id != privateKey:
			return False
		return True

	def ack(self, tid, pid, status):
		pass

	def commit(self):
		pass

class ServerListener:
	def __init__(self):
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
		except OSError:
			self.server.close()
			print('Server closed')

	def stop(self):
		self.server.close()

	def dump(self):
		dumped = self.clients
		self.clients = None
		return dumped

	def removeClient(self, client):
		self.clients.remove(client)

	def foward(self, conn):
		self.clients.append(conn)
		Dispatcher().incoming(conn[0])
		print('Connection established with %s:%d' % conn[1])