class Transaction(object):
    """This is the Transaction object"""

    def __init__(self):
        # Init the object
        self.tid = 0;
        self.value = 0;
        self.time = 0;
        self.giver = Peer(); # Verificate if is right
        self.receiver = Peer(); # Verificate if is right

    def getTId(self):
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

    def setTId(self, TId):
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

    
 