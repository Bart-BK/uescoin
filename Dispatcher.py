import uuid

import socket

class Dispatcher(object):
	"""docstring for Dispatcher"""

	def __init__(self):
		# Create a TCP/IP socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
        # Set socket options
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1);
        CONNECTION = ("", 45678);
		try:
			self.server_socket.bind(CONNECTION);
            self.server_socket.listen(100);
            print("\nListening...");
		except Exception as e:
			print(e);

		

        incoming();

	def incoming(self):
		# Add server socket object to the list of readable connections
        self.socket_list.append(self.server_socket);
