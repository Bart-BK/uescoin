import uuid
import socket #socket
import sys #encode e decode
import time
import calendar
from peer import * #Funcoes
import os #Para detectar o sistema
clear = lambda: os.system('cls' if os.name == 'nt' else 'clear') #Limpar tela

class Peer(object):
	""" Class doc """
	
	def __init__ (self):
		""" Class initialiser """
		self.peer_id = input("Insira seu id: ");
		self.peer_pkey = uuid.uuid4().hex;
		self.peer_balance = 0;

def arquivo_transicoes(tipo_transacao, id):
	if (tipo_transacao == "0"):
		tabelaTransacao = open(id+".txt", 'w+');
		#tabelaTransacao.writelines("tid | data | valor | cedente | receptor | saldoCedente | saldoReceptor\n");
		tabelaTransacao.writelines(uuid.uuid4().hex+" | "+ str(calendar.timegm(time.gmtime())) +" | 100 | system | "+id+" | 0 | 100\n");
		tabelaTransacao.close();
		print("Transacao genesis efetuada");
	else:
		if (not os.path.isfile(id+".txt")):
			tabelaTransacao = open(id+".txt", 'a+');
			tabelaTransacao.writelines(uuid.uuid4().hex+" | "+ str(calendar.timegm(time.gmtime())) +" | 0 | system | "+id+" | 0 | 0\n");
			tabelaTransacao.close();
		else:
			pass;

#def arquivo_chaves_estrangeiras():

def transaction (tid, timestamp, value, giver, receiver, pKey):
	tabelaTransacao = open(giver+"_temp.txt", 'a+');
	#tabelaTransacao.writelines(tid" | "+ timestamp +" | "+value+" | "+giver+" | "+receiver+" | 0 | 0\n"); #fazer leitura inversa do arquivo
	tabelaTransacao.close();

#def ack(tid):

#commit(tid):

def verifica_transacao(peer_id, peer_pkey, value): #falta verificar pkey
	for line in reversed(list(open(peer_id+"_temp.txt"))):
		arrayItems = line.split(' | ');
		if(arrayItems[3] == peer_id):
			if(arrayItems[5] >= value):
				print("Transacao valida");
				return 1;
		elif(arrayItems[4] == peer_id):
			if(arrayItems[6] >= value):
				print("Transacao valida");
				return 1;
		print("Transacao invalida");
		return 0;

def arquivo_transicao_temporaria(id, tid, timestamp, value, giver, receiver, pKey, status):
	tabelaTransacao = open(id+"_temp.txt", 'a+');
	#saldoGiver, saldoReceiver = verifica_saldo(giver, receiver);
	verifica_saldo(giver, receiver);
	saldoGiver = 0;
	saldoReceiver = 0;
	tabelaTransacao.writelines(tid+ " | "+ timestamp +" | "+value+" | "+giver+" | "+receiver+" | "+str(saldoGiver)+" | "+str(saldoReceiver)+" | "+status+"\n");
	tabelaTransacao.close();

def verifica_saldo(giver, receiver):
	saldoGiver = -1;
	saldoReceiver = -1;
	
	for line in reversed(list(open(giver+".txt"))):
		arrayItems = line.split(' | ');
		print(giver+" -> "+str(saldoGiver));
		print(receiver+" -> "+str(saldoReceiver));
		
		'''print(arrayItems[3] + " "+arrayItems[5]);
		print(arrayItems[4] + " "+arrayItems[6]); '''
		if(saldoGiver < 0 or saldoReceiver < 0):
			if (saldoGiver < 0):
				if(arrayItems[3] == str(giver)):
					saldoGiver = int(arrayItems[5]);
				if(arrayItems[4] == str(giver)):
					saldoGiver = int(arrayItems[6]);
			if(saldoReceiver < 0):
				if(arrayItems[3] == str(giver)):
					saldoGiver = int(arrayItems[5]);
				if(arrayItems[4] == str(giver)):
					saldoGiver = int(arrayItems[6]);
		else:	
			return saldoGiver, saldoReceiver;
			
def Programa():
	# Criando socket TCP/IP
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# Conectando o socket com a porta ouvida pelo servidor
	server_address = ("localhost", 5000) #Obtem endereço = host e porta
	print('Conectando ao servidor {} na porta {}'.format(server_address[0], server_address[1]))
	sock.connect(server_address) #conecao
	peer = Peer();
	
	try:
		data = sock.recv(1024) #Receber OK
		data = data.decode();
		print(data);
		
		sock.sendall(peer.peer_id.encode()) #Enviar ID
		
		tipo_transacao = sock.recv(1024) #Receber Tipo de transacao
		tipo_transacao = tipo_transacao.decode();
		arquivo_transicoes(tipo_transacao, peer.peer_id);
		
		while True:
			comando = input("\nO que deseja fazer? ");
			if(comando == "transaction"):
				# do something
				value = input("Insira o valor: ");
				receiver = input("Insira o receiver: ");
				arquivo_transicao_temporaria(peer.peer_id, uuid.uuid4().hex,str(calendar.timegm(time.gmtime())), value, peer.peer_id, receiver, peer.peer_pkey, "pendente");
				if(verifica_transacao(peer.peer_id, peer.peer_pkey, value)):
					print("ack");
					# se todo mundo der ack, chama commit
				else:
					print("nack");
				
			else:
				print("comando não reconhecido\n");
		
		
	finally:
		print('Encerrando o cliente')
		sock.close() #Fecha conexao


#Inicia Programa:
Programa();
