import uuid
import socket
import time
import calendar
import random
from peer import *
import os
clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')

connection_count = 0;

# Cria o socket TCP/IP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Endereco IP do Servidor + Porta que o Servidor esta
server_address = ('localhost', 5000)
sock.bind(server_address)#enviar para rede o meu endereço

# Fica ouvindo por conexoes, apenas um pode se comunicar
sock.listen(100)

#while True:
	# Servidor sempre ativo
clear()
print ("Nome do servidor: localhost")

while True:
	print('Aguardando a conexao...')
	con, cliente = sock.accept()
	connection_count += 1;
	try:
		print('Computador <{}, {}> acaba de se conectar'.format(cliente[0], cliente[1]))
		con.sendall(("Coneccao aceita").encode()) #Enviar OK
		
		data = con.recv(1024) #Receber ID
		data = data.decode();
		
		if(connection_count <= 2): #Enviar Tipo de transacao
			con.sendall(("0").encode()) #genesis
		else:
			con.sendall(("1").encode()) #outro
			
		
	finally:
		# Clean up the connection
		con.close()
