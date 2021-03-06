# Local network config
NET_LOCAL = {
	'HOST':		'192.168.56.101',
	'PORT':		5555,
	'QUEUE': 	5
}

# Known hosts
NET_GROUP = {
	'NEXT':		('192.168.56.1', 5555),
	'PREV':		('192.168.56.1', 5555)
}

# Data
PATH = {
	'PEERS': 	'data/peers.dat',
	'TX_TEMP': 	'data/tx_temp.dat',
	'TX_COMMIT':'data/tx_commited.dat',
	'TX_MINE': 	'data/tx_mine.dat',
	'ACKS': 	'data/acks.dat'
}

PEERS_COUNT = 2

# Approval rule
ACKS_TO_APPROVE = PEERS_COUNT

# Peer ID
WHO_I_AM = 1