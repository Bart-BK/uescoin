class Transaction(object):
    """This is the Transaction object"""

    def __init__(self):
        # Init the object
        self.tid = 0;
        self.value = 0;
        self.time = 0;
        self.giver = Peer(); # Verificate if is right
        self.receiver = Peer(); # Verificate if is right
        self.balanceGiver = 0;
        self.balanceReceiver = 0;

        self.status = 'pendente';

    def getTid(self):
        # Return the self tid
        return self.tid;

    def getValue(self):
        # Return the self value
        return self.value;

    def getTime(self):
        # Return the self time
        return self.time;

    def getGiver(self):
        # Return the self giver
        return self.giver;

    def getReceiver(self):
        # Return the self receiver
        return self.receiver;

    def getBalanceGiver(self):
        # Return the self balance of giver
        return self.balanceGiver;

    def getBalanceReceiver(self):
        # Return the self balance of receiver
        return self.balanceReceiver;

    def getStatus(self):

        return self.status;

    def setTid(self, TId):
        # Set the Tid
        self.tid = TId;

    def setValue(self, value):
        # Set the Value
        self.value = value;

    def setTime(self, time):
        # Set the Time
        self.time = time;

    def setGiver(self, giver):
        # Set the Giver
        self.giver = giver;

    def setReceiver(self, receiver):
        # Set the Receiver
        self.receiver = receiver;

    def setBalanceGiver(self, balanceGiver):
        # Set the self balance of giver
        self.balanceGiver = balanceGiver;

    def setBalanceReceiver(self, balanceReceiver):
        # Set the self balance of receiver
        self.balanceReceiver = balanceReceiver;

    def setStatus(self, status):

        self.status = status;

    ''' Fazer analise se e necessario '''
    def initTempTable(self, tempFile):
        open(tempFile, 'w+');
        # Header of txt
        tabelaTransacao.writelines("tid | data | valor | cedente | receptor | saldoCedente | saldoReceptor");
        # Close txt
        tabelaTransacao.close();

    def insertTempTable(self, tempFile):
        # Create txt
        tabelaTransacao = open(tempFile, 'a');
        # Header of txt
        tabelaTransacao.writelines(self.getTid+" | "+self.getTime+" | "+self.getValue+" | "+self.getGiver+" | "+self.getReceiver+" | "+self.getBalanceGiver+" | "+self.getBalanceReceiver);
        # Close txt
        tabelaTransacao.close();
