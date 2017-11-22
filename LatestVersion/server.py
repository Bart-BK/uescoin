import socket #Conectar 2 peers
import pickle #Serializar
import defs #Definicoes


"""
	Classe Dispatcher
		Responsavel para encaminhar as mensagem recebidas para a conexao
"""
class Dispatcher:
	'''
		Construtor: Recebe quem está aguardando a mensagem
	'''
	def __init__(self, listener):
		self.listener = listener


	'''
		INCOMING: Recebe a conexão e extrai os tokens da menssagem
	'''
	def incoming(self, conn):
		self.conn = conn #Conexao
		params = pickle.loads(conn.recv(4096)) #Deserializar a conexao
		try:
			getattr(self, params[0])(*params[1:]) #Tenta realizar uma chamada com reflexao
		except (TypeError, AttributeError) as e: #Erro
			print('Protocol error. %s: %s' % (type(e).__name__, e))
			conn.send('Protocol error'.encode('UTF-8'))

	'''
		DISPACTCH: Responsavel por enviar uma resposta
	'''
	def dispatch(self, *protocol):
		self.conn.send(pickle.dumps(protocol))
		self.conn.close()
		self.listener.removeClient(self.conn)




"""
	Classe ServerListener
"""
class ServerListener:
	'''
		Construtor
	'''
	def __init__(self, dispatcher):
		self.dispatcher = dispatcher
		self.server = None
		self.clients = []

	'''
		START: Ele pode receber o host, a porta e o tamanho da fila do socket (opcionais)
	'''
	def start(self, HOST = defs.HOST, port = defs.PORT, queueSize = defs.QUEUE_SIZE):
		try:
			self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Inicia a listener na porta
			self.server.bind((HOST, port))
			self.server.listen(queueSize)
			print('Server started on %s:%d' % (HOST, port))
			while True:
				client = self.server.accept()
				self.forward(client)
		except OSError as e:
			self.server.close()
			print('Server closed: ', e)

	'''
		STOP
	'''
	def stop(self):
		self.server.close()

	'''
		DUMP: Despeja as conexoes, retornando-as
	'''
	def dump(self):
		dumped = self.clients
		self.clients = None
		return dumped

	'''
		REMOVE CLIENT
	'''
	def removeClient(self, client):
		self.clients.remove(client)

	'''
		FORWARD: Encaminha a conexao para o Dispacher, adiccionando no pool
	'''
	def forward(self, conn):
		conn, addr = conn
		self.clients.append(conn)
		self.dispatcher(self).incoming(conn)
		print('Connection established with %s:%d' % addr)