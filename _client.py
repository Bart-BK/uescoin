# Import from sys 
from sys import argv, stdin, stdout
# Import sockets
import socket
# Import select
import select
# Import UUID
import uuid
# Import os (to clear function)
import os
clear = lambda: os.system('cls' if os.name == 'nt' else 'clear') #Limpar tela

# Client socket
class Client_UESCOIN:
	"""This is a client who is connected with the socket server and is client of blockchain"""

	def __init__(self):
		# Create a TCP/IP socket
		self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
		# Set timeout connection
		self.client_socket.settimeout(10);
	
	def get_HOST_PORT(self):
		# Case HOST and PORT given by command line
		if(len(argv) == 3):
			HOST = argv[1];
			PORT = argv[2];
		# Else, request the input for the HOST and PORT
		else:
			print("Failed to get the HOST and PORT\n");
			HOST = input("Enter the HOST: ");
			PORT = input("Enter the PORT: ");

		# Return the HOST and PORT
		return HOST,PORT;

	def connect(self, HOST, PORT):
		# Define connection
		try:
			CONNECTION = (HOST, int(PORT));
		except:
			# If CONNECTION not receive an int
			while(self.isNotInt(PORT, "PORT")):
				PORT = input("Enter the PORT (must be int): ");
			CONNECTION = (HOST, int(PORT));

		print("Connecting to "+HOST+"::"+PORT);

		try:
			# Try connect in HOST and PORT given
			self.client_socket.connect(CONNECTION);
			print("Connection established...");

		except:
			print ("Error in connection "+HOST+"::"+PORT);
			# If have any trouble, try receive again
			choice = input("[A]bort, [C]hange ou [T]ry again?");
			# Choice is abort
			if(choice.lower() == "a"):
				exit();
			# Choice is change
			elif(choice.lower() == "c"):
				HOST = input("Enter the HOST: ");
				PORT = input("Enter the PORT: ");
			
			self.connect(HOST,PORT);

	"""
	def clear(self):
		# Clear the console (works in linux and windows)
		os.system('cls' if os.name=='nt' else 'clear');
	"""
	
	def recv(self, sock):
		# Receive a message from socket
		return sock.recv(4096);
	
	def start(self):

		while 1:
			# Socket list [key, value]
			socket_list = [stdin, self.client_socket];

			# Get the list sockets which are readable
			ready_to_read,ready_to_write,in_error = select.select(socket_list , [], []);
		     
			for sock in ready_to_read:
				# If sock is this client        
				if sock == self.client_socket:
					# Incoming position from remote server

					# Receive the message
					data = self.recv(sock);
					# Decode the received data
					data = data.decode();

					if not data :
						# Some trouble ...
						print ('\nDisconnected from blockchain\n');
						exit();
					else :
						# Clear the console
						#self.clear();
						try:
							# If received a block command, dont print the command
							# Here is where the commands will be received, if print, will print
							
							#Receive and set the ID
							if(data[0:5] == "[PID]"):
								self.id = data[5:10];
								self.init_Transactions_Table();
								print(data[10:]);
							else:
								# Print message
								print(data);
							

						except Exception as e:
							print(str(e));
						

				else :
					# Here is where the command insertion will be prompted
					
					# Clear buffer
					stdout.flush();
	
	# Init the transactions table
	def init_Transactions_Table(self):
		tabela = open(self.id+".txt", 'w+');
		tabela.writelines("data | valor | cedente | receptor | saldoCedente | saldoReceptor\n");
		tabela.close();

	# Init the ids table
	def init_Id_Table(self):
		print("Nao implementado ainda");

	def commit(self, tid):
		#data.encode()
		print("Nao implementado ainda");
	
	def transaction(self, tid, timestamp, value, giver, receiver, pkey):
		print("Nao implementado ainda");
	
	
def main():
	title = "          _______  _______  _______  _______ _________ _       \n"\
			" |\     /|(  ____ \(  ____ \(  ____ \(  ___  )\__   __/( (    /|\n"\
			" | )   ( || (    \/| (    \/| (    \/| (   ) |   ) (   |  \  ( |\n"\
			" | |   | || (__    | (_____ | |      | |   | |   | |   |   \ | |\n"\
			" | |   | ||  __)   (_____  )| |      | |   | |   | |   | (\ \) |\n"\
			" | |   | || (            ) || |      | |   | |   | |   | | \   |\n"\
			" | (___) || (____/\/\____) || (____/\| (___) |___) (___| )  \  |\n"\
			" (_______)(_______/\_______)(_______/(_______)\_______/|/    )_)\n"\
			"                                                                \n";

	welcome_message =	"\n\n(1) Start the blockchain simulator\n"\
						"(2) Credits\n"\
						"(3) Quit\n\n";

	# Display a welcome message
	choice = input(title + welcome_message);

	while True:
		try:
			# Start the game
			if(int(choice) == 1):
				# Main class of Tic Tac Toe
				client = Client_UESCOIN();

				# Get the HOST and PORT
				HOST, PORT = client.get_HOST_PORT();

				# Try connect
				client.connect(HOST,PORT);

				# Start the Player socket
				client.start();

				exit();

			# Show Credits
			elif(int(choice) == 2):
				credits = "UESCOIN made by:\n\nPrabhat Kumar de Oliveira\nEberty Alves da Silva\nIago Farias\n";
				choice = input(title + credits + welcome_message);

			# Exit
			elif(int(choice) == 3):
				print("Exiting...\n");
				exit();

			# Invalid choice (if int)
			else:
			    while((int(choice) < 1) or (int(choice) > 3)):
			        choice = input("Please, enter valid choice: ");

        # Invalid choice (if not int)
		except Exception as e:
			choice = input("Invalid choice, please enter again (must be int): ");
	

if __name__ == "__main__":
    #os.system('cls' if os.name=='nt' else 'clear');
    clear();
    main();
