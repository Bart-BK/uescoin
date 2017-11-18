import pickle

class Peer:
	def __init__(self):
		self.id = None
		self.balance = None
		self.privateKey = None

	@staticmethod
	def find(filePath, id):
		fin = open(filePath, 'rb')
		tx_dict = pickle.load(fin)
		fin.close()
		for k, tx in tx_dict.items():
			if tx.giver.id == id:
				return tx.giver
			if tx.receiver.id == id:
				return tx.receiver

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
		tx_dict = pickle.load(fin)
		return tx_dict[id]

	@staticmethod
	def save(filePath, tx):
		fin = open(filePath, 'rb')
		tx_dict = pickle.load(fin)
		tx_dict[tx.id] = tx
		fin.close()
		fout = open(filePath, 'wb')
		pickle.dump(tx_dict, fout)
		fout.close()

	@staticmethod
	def remove(filePath, tx):
		pass

def addAck(filePath, tid, pid, status):
	fin = open(filePath, 'rb')
	ack_dict = pickle.load(fin)
	fin.close()
	ack_dict[tid] = pid, status
	fout = open(filePath, 'wb')
	pickle.dump(ack_dict, fout)
	return len(ack_dict)