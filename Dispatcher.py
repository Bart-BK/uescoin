
import socket

import select

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

		while True:
			self.incoming();

	def incoming(self):
		self.socket_list = [];
		# Add server socket object to the list of readable connections
		self.socket_list.append(self.server_socket);
		# Get the list sockets which are ready to be read through select
		ready_to_read,ready_to_write,in_error = select.select(self.socket_list,[],[],0);

		for sock in ready_to_read:
			# A new connection request recieved
			if sock == self.server_socket:
				# Accept the connection
				sockfd, addr = self.server_socket.accept();
				self.socket_list.append(sockfd);

				message = "Oi";
				sockfd.send(message.encode());
				print ("recebendo")
				# Receive the message
				data = sockfd.recv(1024);
				print("recebido")
				# Decode the received data
				data = data.decode();
				print(data);
			else:
				try:
					#sock.send(("Hello World").encode());
					# If received a command
					data = sock.recv(1024);
					if data: # and its data
						print("recebendo dados");
						#arrayItems = data.split(' | ');
					else: # if is not data, some trouble happens, so kill them
						#self.socket_list.remove(sock);
						pass
				except:
					pass;

if __name__ == "__main__":
	print("Hello World");
	dispatcher = Dispatcher();
