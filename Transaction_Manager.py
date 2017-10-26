class Transaction_Manager(object):
    """This is the Transaction object"""

    def __init__(self, fileTemp):
        # Init the object
        self.file = fileTemp;
        # Create the file
        open(self.file, 'w+');
        # Header of txt
        tabelaTransacao.writelines("tid | data | valor | cedente | receptor | saldoCedente | saldoReceptor");
        # Close txt
        tabelaTransacao.close();

    def insertTableTemp(self, transaction):
        # Create txt
        tabelaTransacao = open(self.file, 'a');
        # Header of txt
        tabelaTransacao.writelines(transaction.getTid+" | "+transaction.getTime+" | "+transaction.getValue+" | "+transaction.getGiver+" | "+transaction.getReceiver+" | "+transaction.getBalanceGiver+" | "+transaction.getBalanceReceiver);
        # Close txt
        tabelaTransacao.close();

    
 