class Peer(object):
    """This is the PEER object"""

    def __init__(self):
        # Init the object
        self.id = 0;
        self.privateKey = 0;
        #self.balance = 0;

    def getId(self):
        # Return the self id
        return self.id;

    def getPrivateKey(self):
        # Return the self private key
        return self.privateKey;

    '''
    def getBalance(self):
        # Return the self balance
        return self.balance;
    '''

    def setPrivateKey(self, privateKey):
        # Set the private key
        self.privateKey = privateKey;

    '''
    def setBalance(self, balance):
        # Set the balance
        self.balance = balance;
    
    def toString(self):
        # Return the self id with the self private key and the self balance
        return self.id + " " + self.privateKey + " " + self.balance;
    '''
    
 