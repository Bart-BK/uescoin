from server import ServerListener
from transaction import TransactionDispatcher

ServerListener(TransactionDispatcher).start()