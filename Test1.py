# Import sockets
import socket
# Import select
import select
# Import from sys
from sys import argv, stdin, stdout

class Test1(object):
	"""docstring for ClassName"""
	def __init__(self):
		print("OK");
		self.main();

	def main(self):
		# Create a TCP/IP socket
		self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
		# Set timeout connection
		self.client_socket.settimeout(10);
		CONNECTION = ("localhost", 45678);

		try:
			self.client_socket.connect(CONNECTION);
			print("Sucesso");
			self.receiving();
		except Exception as e:
			print(e);

	def receiving(self):
		while True:

			# Socket list [key, value]
			socket_list = [stdin, self.client_socket];
			# Get the list sockets which are readable
			ready_to_read,ready_to_write,in_error = select.select(socket_list , [], []);

			for sock in ready_to_read:
				# If sock is this client
				if sock == self.client_socket:
					# Incoming position from remote server

					# Receive the message
					data = sock.recv(1024);
					# Decode the received data
					data = data.decode();

					if not data :
						# Some trouble ...
						#print ('\nDisconnected from blockchain\n');
						#exit();
						#message = "NACK";
						#sock.send(message.encode());
						pass
					else :
						print(data);

						if(input() == "ack"):
							message = "ACK";
							sock.send(message.encode());
						else:
							print("comando nao reconhecido");
						#sockfd.send(message.encode());

if __name__ == "__main__":
	test = Test1();
