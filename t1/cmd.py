from globl import *
import pickle
import blockchain

def openDic(filePath):
	with open(filePath, 'rb') as fin:
	    return pickle.load(fin);

def printAcks(filePath):
    txDict = openDic(filePath)
    for txId, ackDic in txDict.items():
        for peerId, value in ackDic.items():
            print(txId, peerId, value, sep = ' | ')

def printPeers(filePath):
    peers = openDic(filePath)
    print('ID', 'BALANCE', 'PRIVATE KEY', sep = ' | ')
    for p in peers.values():
        print(p.id, p.balance, p.privateKey, sep = ' | ')

def printTransaction(filePath):
    txDic = openDic(filePath)

    for tx in txDic.values():
    	print(tx.id, tx.time, tx.value, 
    		tx.giver.id, tx.giver.balance, 
    		tx.receiver.id, tx.receiver.balance,
    		sep = ' | ')

def info():
    peer = find(PATH['PEERS'], WHO_I_AM)
    print(
        'ID:\t\t%d'
        'Balance:\t%.2f',
        (WHO_I_AM, peer.balance))