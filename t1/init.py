from globl import *
from data import *

def init():
	print('Initializing...')

	# Genesis transaction
	# Preset peer
	p0 = Peer()
	p0.id = 0
	p0.balance = 100
	p0.privateKey = 0

	tx = Transaction()
	tx.id = 0
	tx.time = 0
	tx.value = 100
	tx.giver = p0
	tx.receiver = p0

	transactions = {tx.id: tx}
	peers = {p0.id: p0}

	# Other known peers
	for i in range(1, 10):
		p = Peer()
		p.id = i
		p.balance = 0
		p.privateKey = i
		peers[i] = p

	# Creating data files

	# Temporary transactions
	initData(PATH['TX_TEMP'], {})
	# Commited transactions
	initData(PATH['TX_COMMIT'], transactions)
	# Own transactions
	initData(PATH['TX_MINE'], {})
	# Peers
	initData(PATH['PEERS'], peers)
	# Acknowledgements
	initData(PATH['ACKS'], {})

	print('')