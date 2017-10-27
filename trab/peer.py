#coding: utf-8
from random import * #aleatorio

def lerLinhas():
	print('\n\n***********NIM***********\n O jogo dos palitos!\n')
	# Cria um tabuleiro de jogo vazio
	linpali = 0;
	while(linpali < 4 or linpali > 30):
		w =  input('Entre com a quantidade de linhas de palitos: ')
		try:
			linpali =  int(w)
		except:
			linpali = 0
	return linpali;


def lerLinQtd():
	x = input('Digite a linha: ')
	try:
		lin = int(x)
	except:
		lin = 0
	
	x = input('Diga a qtd de palitos: ')
	try:
		qtd = int(x)
	except:
		qtd = 0
	
	return lin, qtd



# -------------------------------------------------
class Jogo:
	# Classe que representa o estado do jogo.

	def __init__(self, linpali):
		'''
		Construtor: Inicializa o jogo
		
		Atributos da clase:
			linpali = Quantidade de linhas (fileiras com palitos)
			v = Vetor (que terá tamanho linpali) contendo a auntidade de palitos para cada linha ainda restantes
			tot = Qantidade total de palitos ainda restantes do jogo, é usado para definir o fim de jogo
		'''
		self.jogando = True;
		self.linpali = linpali
		self.v = []
		self.tot = 0
		for i in range(1, linpali+1):
			self.tot = self.tot + i
			self.v.append(i)
		self.jogador = 1 #Primeiro = 0, pois ele troca na primeira printagem, antes da jogada

	# -------------------------------------------------
	def salva(self):
		'''
		O QUE FAZ: Salva os dados do jogo.
			 
		OBJETIVO: Gera um estado de jogo a ser passado (string - pois nao pode passar o vetor),
				  Ele é identicado pelos valores contidos em cada x em self.v separados por espaços
				  Assim, o estado do jogo pode ser comunicado via socket.

		RETORNO: O estado atual do tabuleiro (em formato nao vetor).
		'''
		a = ''
		for i in range(0, self.linpali):
			a = a + str(self.v[i]) + " "
		return a


	# -------------------------------------------------
	def restaura(self, data):
		'''
		O QUE FAZ: Restaura os dados do jogo (Após uma jogada) a partir do dado informado pelo soket.

		OBJETIVO: Atualiza o estado do jogo, de forma que após a restauração ele possua a nova quantidade depalitos restantes por linha.

		RETORNO: Não há retorno.
		'''
		self.v = [int(x) for x in data.split()]
		self.tot = 0
		for i in range(0, self.linpali):
			self.tot += self.v[i]
	

	# -------------------------------------------------
	def printa_jogo(self):
		'''
		O QUE FAZ: Imprime o tabuleiro em um formato visual.
		
		OBJETIVO: Capaz de tornar o jogo visualmente intendivel
		
		RETORNO: Não há retorno.		
		'''
		#if (self.jogador == 0):
		#	print ("Jogador = Cliente")
		#else:
		#	print ("Jogador = Servidor")
			
		for i in range(0, self.linpali):
			a = str(i+1) + " -"
			for j in range(0, self.v[i]):
				a = a + " |"
			print (a)
		print("\n")

		# Fazer Funcao que define o ganhador
		if (self.tot < 2):
			print ('Parece que temos um CAMPEÃO e um PERDEDOR');
			self.ganhador()
			self.jogando =  False


	# -------------------------------------------------
	def jogada(self, lin, qtd):
		'''
		O QUE FAZ: Faz uma jogada, utilizando-se das posições e quantidades informadas.

		OBJETIVO: Realizar jogada, removendo a quantidade de palitos ou apresntando erro se a informação for inválida.

		RETORNO: Não há retorno.
		'''
		# Valida os parâmetros de entrada
		if (qtd > self.v[lin-1] or qtd < 1 or lin > self.linpali or lin <= 0):
			raise RuntimeError('Número de linha ou quantidade inválidos')
		# Faz a jogada
		self.v[lin-1] = self.v[lin-1] - qtd;
		self.tot = self.tot - qtd;
	
	
	# -------------------------------------------------
	def jogadaAleatoria(self):
		'''
		O QUE FAZ: Realiza uma remoção de palitos aleatória, atavés de uma jogada válida para  aquele  estado de jogo
		
		OBJETIVO: Realizar jogada, removendo uma certa quantidade de palitos de uma coluna aleatoriamente
				  Ocorre uma validação dos erros para não ocorrerem durante uma jogada aleatóra (while).

		RETORNO: Não há retorno, chama o metodo jogada.
		'''
		lin = -1
		qtd = 0
		while(qtd > self.v[lin-1] or qtd < 1 or lin > self.linpali or lin <= 0):
			lin = randint(1, self.linpali)
			try:
				qtd = randint(1, self.v[lin-1])
			except:
				qtd = -1	
		self.jogada(lin, qtd)


	# -------------------------------------------------
	def ganhador(self):
		if (self.jogador == 0):
			jog = "Cliente"
		else:
			jog = "Servidor"
		
		if(self.tot == 0):
			print ("\nO ", jog, " PERDEU POR ESTUPIDEZ!!!! Pois ele removeu o ultimo palito\n")
		else:
			print ("\nO ", jog, " venceu! Pois não foi ele que ficou com o ultimo palito\n")
