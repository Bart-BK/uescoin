import pickle
import defs
from server import Dispatcher

"""
	Sub-classe do Dispatcher
"""
class TransactionDispatcher(Dispatcher):
	'''
		Construtor: Recebe quem está aguardando a mensagem
	'''
	def __init__(self, listener):
		#super(self, TransactionDispatcher).__init__(listener)
		self.isMine = False

	'''
		Transaction: Processa uma transacao,
			Checa se a trancasao foi enviada pelo autor da mesma e se ha balanço em sua conta,
			Se isso acontecer, salva os dados no arquivo temporario e chama o ack.
	'''
	def transaction(self, tId, time, value, giverId, receiverId, privateKey):
		print('Incoming transaction: id', tId)
		giver = Peer.find(defs.TX_COMMIT, giverId)
		transfer = giver.balance - value
		if (self.checkPeerKey(giver, privateKey) and transfer >= 0):
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
			self.ack(tId, True)
		else:
			self.ack(tId, False)

	'''
		checkPeerKey
	'''
	def checkPeerKey(self, peer, privateKey):
		if peer.id != privateKey:
			return False
		return True

	'''
		ack:
			Primeiro ele checa se transaction é dele:
				se nao for, ele repassa
				se nao, ele adiciona na lista de acks
				se todos os acks forem recebidos de todos os peers e nao haverem nacks, entao ele envia um commit positivo
	'''
	def ack(self, tId, accepted):
		tx = Transaction.find(defs.TX_MINE, tId)
		if tx == None:
			# Not is mine
			self.dispatch('ack', accepted)
		else:
			# Is mine
			isMine = True
			finout = open(defs.ACKS, 'rb')
			dictAcks = pickle.load(finout)
			if len(dictAcks) == defs.MAX_ACKS:
				commit(tx, False in dictAcks.values())


	'''
		COMMIT
	'''
	def commit(self, tx, accepted):
		pass




"""
	Classe Peer
		Represnta um peer
"""
class Peer:
	def __init__(self):
		self.id = None
		self.balance = None
		self.privateKey = None

	@staticmethod
	def find(filePath, id):
		fin = open(filePath, 'rb')
		txDict = pickle.load(fin)
		fin.close()
		for k, tx in txDict.items():
			if tx.giver.id == id:
				return tx.giver
			if tx.receiver.id == id:
				return tx.receiver


"""
	Classe Transação: contem todas as operacoes
"""
class Transaction:
	def __init__(self):
		self.id = None
		self.time = None
		self.value = None
		self.giver = None
		self.receiver = None

	@staticmethod
	def find(filePath, id):
		fin = open(filePath, 'rb')
		txDict = pickle.load(fin)
		return txDict.get(id)

	@staticmethod
	def save(filePath, tx):
		finout = open(filePath, 'rb+')
		txDict = pickle.load(finout)
		txDict[tx.id] = tx
		pickle.dump(txDict, finout)
		finout.close()

	@staticmethod
	def remove(filePath, tx):
		finout = open(filePath, 'rb')
		txDict = pickle.load(finout)
		txDict.pop(tx.id, None)
		pickle.dump(txDict, finout)
		finout.close()	