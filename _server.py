# Import sockets
import socket
# Import select
import select
# Import argv
from sys import argv 
# Import random (to select who starts)
import random
# Import os (to clear function)
import os
clear = lambda: os.system('cls' if os.name == 'nt' else 'clear') #Limpar tela


class Server_UESCOIN:
    """This is the server, and the logic of the blockchain"""

    def __init__(self):
        # Create a TCP/IP socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
        # Set socket options
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1);
        # Array of sockets
        self.socket_list = [];

    def get_PORT(self):
        # The HOST can bind all (not necessary especific host);
        HOST = "";

        # If parameters is given
        if(len(argv) == 2):
            PORT = argv[1];
        else:
            print("Failed to get the PORT\n");
            PORT = input("Enter the PORT: ");

        # Return the HOST and PORT
        return HOST,PORT;

    def bind(self, HOST, PORT):
        # Define connection
        try:
            CONNECTION = (HOST, int(PORT));
        except:
            # If CONNECTION not receive an int
            while(self.isNotInt(PORT)):
                PORT = input("Enter the PORT (must be int): ");
            CONNECTION = (HOST, int(PORT));

        while True:
            # Try bind
            try:
                self.server_socket.bind(CONNECTION);
                self.server_socket.listen(100);

                print("Bind done, waiting for clients...");
                break;

            except Exception as e:
                # If have any trouble
                print ("There is an error in bind "+PORT+ str(e));
                choice = input("[A]bort, [C]hange ou [T]ry again?");

                # If choice is abort
                if(choice.lower() == 'a'):
                    exit();
                # If choice is change
                elif(choice.lower() == 'c'):
                    PORT = input("Enter the PORT: ");

                self.bind(HOST,PORT);


    def close(self):
        # Close the socket server
        self.server_socket.close();

    def start(self):
        # Add server socket object to the list of readable connections
        self.socket_list.append(self.server_socket);
        
        while True:
            # Get the list sockets which are ready to be read through select
            ready_to_read,ready_to_write,in_error = select.select(self.socket_list,[],[],0);

            for sock in ready_to_read:
                # A new connection request recieved
                if sock == self.server_socket: 
                    # Accept the connection
                    sockfd, addr = self.server_socket.accept();
                    
                    self.socket_list.append(sockfd);

                    print("Player (%s, %s) connected" % addr);

                    # Get IP connection and Socket ID
                    sockip, sockid = addr;
                    self.broadcast( self.server_socket, sockfd, str(sockid));

    def main_loop(self):
        
        RECV_BUFFER = 1024;

        ''' Here is where the logic of blockchain will be implemented '''

    # broadcast messages to all connected clients
    def broadcast (self, server_socket, target, message):
        for socket in self.socket_list:
            # send the message only to peer
            if socket != server_socket:
                try :
                    #If socket is not itself
                    if(socket != target):
                        socket.send(("Peer "+message+" conectado").encode());
                    else:
                        socket.send(("[PID]"+message+"Bem vindo ao UESCOIN").encode());
                except :
                    # broken socket connection
                    socket.close();
                    # broken socket, remove it
                    if socket in self.socket_list:
                        self.socket_list.remove(socket);
 
 
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

    welcome_message =   "\n\n(1) Start host for the blockchain simulator\n"\
                        "(2) Credits\n"\
                        "(3) Quit\n\n";

    # Display a welcome message
    choice = input(title + welcome_message);

    while True:
        try:
            # Start host
            if(int(choice) == 1):
                # Main class of the Tic Tac Toe Server
                server = Server_UESCOIN();

                # Get the HOST and PORT
                HOST, PORT = server.get_PORT();

                # Try bind
                server.bind(HOST, PORT);

                # Start the Server socket
                server.start();

                # Close the Server socket
                server.close();

                exit();

            # Show credits
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
            print(str(e));

if __name__ == "__main__":
    #os.system('cls' if os.name=='nt' else 'clear');
    clear();
    main();
