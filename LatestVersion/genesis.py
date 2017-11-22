import defs #Importa meu arquivo de Definicoes
import pickle #Serializar os Objetos
import transaction #Importa Meu Tansaction
import uuid #Chave
import time #Tempo

'''
	Transacao genesis é a trancacao que inicia a economia da moeda, gerando o balanco para as trancacoes futuras
'''


# Transaction 1
'''
	Coloca a primeira unidade monetaria no peer zero:
		Criando o primeio peer que vai servir como fonte inicial e setando seus valores: ID, Saldo e sua chave privada
		Agora que o primeiro peer está criado, o recebedor inicial é setado como sendo ninguem
		É realizada a trancacao dados o Peer e o Receiver
'''

giver1 = transaction.Peer()
giver1.id = 0
giver1.balance = 100
giver1.privateKey = 0

receiver1 = transaction.Peer()
receiver1.id = None
receiver1.balance = None
receiver1.privateKey = None

tx1 = transaction.Transaction()
tx1.id = uuid.uuid4().int
tx1.time = time.time()
tx1.value = 0
tx1.giver = giver1
tx1.receiver = receiver1

#Transaction 2
'''
	Coloca a primeira unidade monetaria no peer zero:
		Similar a trancacao 1
'''
giver2 = transaction.Peer()
giver2.id = 0
giver2.balance = 50
giver2.privateKey = 0

receiver2 = transaction.Peer()
receiver2.id = 1
receiver2.balance = 0
receiver2.privateKey = 1

tx2 = transaction.Transaction()
tx2.id = uuid.uuid4().int
tx2.time = time.time()
tx2.value = 50
tx2.giver = giver2
tx2.receiver = receiver2


'''
	Agora é nescessario Commitar para gravar no arquivo para validar diretamente a transacao genesis
'''
fout = open(defs.TX_COMMIT, 'wb')
pickle.dump({tx1.id: tx1, tx2.id: tx2}, fout)
fout.close()

fout = open(defs.TX_MINE, 'wb')
pickle.dump({}, fout)
fout.close()

fout = open(defs.TX_TEMP, 'wb')
pickle.dump({}, fout)
fout.close()

#tx3 = transaction.Transaction.find(defs.TX_COMMIT, tx1.id)
#tx4 = transaction.Transaction.find(defs.TX_COMMIT, tx2.id)
#print(tx3.id, tx3.time, tx3.value, tx3.giver.id, tx3.receiver.id, sep = '|')
#print(tx4.id, tx4.time, tx4.value, tx4.giver.id, tx4.receiver.id, sep = '|')