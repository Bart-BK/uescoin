# Import from sys
from sys import argv, stdin, stdout
# Import sockets
import socket
# Import select
import select
# Import time
import time # For timestamp
# Import UUID
import uuid # For generate random ID
# Import os (to clear function)
import os
clear = lambda: os.system('cls' if os.name == 'nt' else 'clear') #Cear screen


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

	def isNotInt(self, value):
		try:
			if(int(value) > 0):
				return False;
			return True;
		except: # The value isn't a int type
			return True;

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
			print ("Aborting...\n")
			exit();
			"""
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

							# Receive and set the ID
							if(data[0:5] == "[PID]"):
								# SET my ID
								self.id = data[5:10];
								# Create Table of transactions
								self.init_Transactions_Table();
								# Create Table of IDS
								self.init_ID_Table();
								# Show MY ID
								print(data[10:]);
								# Generate my PKEY (Public Key)
								self.pKey  = uuid.uuid4().int;
								# Show my PKEY
								print("My pKey: "+self.getPKey());
								tupleKey = self.id+"  | "+self.getPKey();
								# Give PKey to server (PUBLIC KEY)
								sock.sendall(tupleKey.encode());

							# Receive new ID
							elif (data[0:5] == "[UID]"):
								# IF has new ID, add in my txt of ids
								self.add_in_ID_Table(data[5:]);

							else:
								# If is not a command, Print message
								print(data);

						except Exception as e:
							print(str(e));

				else :
					# Here is where the command insertion will be prompted
					# Clear buffer
					# If i want a transaction, write 'transaction'
					if input() == "transaction":
						# Get value
						value = input("Enter the value: ");
						# Get receiver
						receiver = input("Enter receiver code: ");
						# Call the transaction function
						self.transaction(uuid.uuid4().hex,time.time(), value, self.id, receiver, self.pKey);
					# Clear buffer
					stdout.flush();

	# Get PKey
	def getPKey(self):
		return str(self.pKey);

	# Init the transactions table
	def init_Transactions_Table(self):
		# Create txt
		tabelaTransacao = open(self.id+".txt", 'w+');
		# Header of txt
		tabelaTransacao.writelines("data | valor | cedente | receptor | saldoCedente | saldoReceptor\n");
		# Close txt
		tabelaTransacao.close();

	# Init the ids table
	def init_ID_Table(self):
		# Create txt
		tabelaID = open(self.id+"_keys.txt", 'w+');
		# Header of txt
		tabelaID.writelines("peerID | pKey\n");
		# Close txt
		tabelaID.close();

	# Add new peer's id to table of ids
	def add_in_ID_Table(self, data):
		# Open txt
		tabelaID = open(self.id+"_keys.txt", 'a');
		# Add to end of file
		tabelaID.writelines(data+"\n");
		# Close txt
		tabelaID.close();

	def commit(self, tid):
		#data.encode()
		#mandar pro servidor
		#esperar o ack
		print("\nDon't implemented yet");

	def transaction(self, tid, timestamp, value, giver, receiver, pkey):
		clear(); # Clear the console
		print("Transaction in progress\n"); # Show message
		print("Transaction ID "+tid+"\n"); # Show TID

		# verificar pkey chama como função
		if(giver == self.id and pkey == self.pKey): # Check if was me who called the function
			transacaoValida = False; # Set a flag !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! NAO FUNCIONA AINDA
			for line in reversed(list(open(self.id+".txt"))): # Read the file bottom up
				arrayItems = line.split(' | '); # Split the file headers and values
				#("data | valor | cedente | receptor | saldoCedente | saldoReceptor\n");
				#   0  	| 	1	|	2	  |		3	 | 		4 		| 		5
				# 0 | 0 | AQUI_VAI_O_ID | 20 | 200 | 0 # Colocar isso no arquivo
				# Only print to check
				#print(arrayItems[3]);
				#print(arrayItems[2]);
				#print("ID : "+self.id);
				# It was to be "If i'm a receiver recently"
				if(arrayItems[3] == self.id):
					# And if i have money
					if(int(arrayItems[5]) >= int(value)):
						print(arrayItems[5]);
						#print("You have money enough\n");
						transacaoValida = True; # Set flag on
				# It was to be "If i'm a giver"
				elif(arrayItems[2] == self.id):
					# But i have cash yet
					if(int(arrayItems[4]) >= int(value)):
						#print("You have money enough\n");
						transacaoValida = True; # Set flag on

			if(transacaoValida == False): # If flag is off
				print("Sorry, you don't have money enough\n");
			else:
				print("Transaction effected with success\n");


def main():
	title = "           _______  _______  _______  _______ _________ _       \n"\
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
						"(3) Quit\n"\
                        "\nYour Choice: ";

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
				clear();
				credits = "UESCOIN made by:\n\nPrabhat Kumar de Oliveira\nEberty Alves da Silva\nIago Farias Santana\n\nPress Enter to continue...\n\n";
				aux = input(title + credits)
				clear();
				choice = input(title + welcome_message);

			# Exit
			elif(int(choice) == 3):
				clear();
				print("Exiting...\n");
				exit();

			# Invalid choice (if int)
			else:
			    while((int(choice) < 1) or (int(choice) > 3)):
			        choice = input("Please, enter valid choice: ");

        # Invalid choice (if not int)
		except Exception as e:
			choice = input("Invalid choice, please enter again (must be int): ");
			print(e);


if __name__ == "__main__":
    clear();
    main();
