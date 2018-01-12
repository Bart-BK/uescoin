#!/usr/bin/env python3

from globl import NET_LOCAL
from network import ServerListener
from blockchain import TransactionDispatcher
import init

def main():
	init.init()
	server = ServerListener(TransactionDispatcher)

	try:
		server.start(NET_LOCAL['HOST'], NET_LOCAL['PORT'], NET_LOCAL['QUEUE'])
	except KeyboardInterrupt:
		server.stop()

	exit()

if __name__ == "__main__": main()