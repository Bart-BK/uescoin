import pickle
import os.path
from collections import Counter

class Peer:
	def __init__(self):
		self.id = None
		self.balance = None
		self.privateKey = None

class Transaction:
	def __init__(self):
		self.id = None
		self.time = None
		self.value = None
		self.giver = None
		self.receiver = None

class AckHandler:
	def __init__(self, filePath, tId):
		self.filePath = filePath
		self.tId = tId
		self.txDict = None
		self.approved = None
		self.rejected = None
		self.count = None
		self.load()

	def load(self):
		with open(self.filePath, 'rb') as fin:
			self.txDict = pickle.load(fin)

		ackDict = self.txDict.get(self.tId, {})
		values = dict(Counter(ackDict.values()))
		self.approved = values.get(True, 0)
		self.rejected = values.get(False, 0)
		self.count = self.approved + self.rejected

	def add(self, peerId, approved):
		ackDict = self.txDict.get(self.tId, {})
		ackDict[peerId] = approved
		self.txDict[self.tId] = ackDict

		with open(self.filePath, 'wb') as fout:
			pickle.dump(self.txDict, fout)

		self.load()

	def clear(self):
		self.txDict.pop(self.tId, None)
		
		with open(self.filePath, 'wb') as fout:
			pickle.dump(self.txDict, fout)
		
		self.load()

def initData(filePath, data):
	if not os.path.isfile(filePath):
		with open(filePath, 'wb') as file:
			print('Creating', filePath)
			pickle.dump(data, file)
	else:
		print(filePath, 'found')

def find(filePath, id):
	with open(filePath, 'rb') as fin:
		dic = pickle.load(fin)
		return dic.get(id, None)

def save(filePath, obj):
	with open(filePath, 'rb') as fin:
		dic = pickle.load(fin)

	dic[obj.id] = obj

	with open(filePath, 'wb') as fout:
		pickle.dump(dic, fout)

def remove(filePath, id):
	with open(filePath, 'rb') as fin:
		dic = pickle.load(fin)

	obj = dic.pop(id, None)

	with open(filePath, 'wb') as fout:
		pickle.dump(dic, fout)
		return obj

def checkPeerKey(peer, privateKey):
	return peer.id == privateKey