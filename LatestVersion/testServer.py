from server import ServerListener
from transaction import TransactionDispatcher

"""
	Inicia o listener com uma sub-classe de Dispatcher
"""
ServerListener(TransactionDispatcher).start()