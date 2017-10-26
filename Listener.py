import select

class Listener(object):
	"""docstring for Listener"""
	def __init__(self):
		# Array of sockets
        self.socket_list = [];

		listener();

	def listener(self):

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
                sockip, sockid = addr; # Get HOST and PORT (the port will be the peer ID)
                # [PID] = Peer ID
                #erro
                self.broadcast( self.server_socket, sockfd, "[PID]"+str(sockid)+"Welcome to UESCOIN");
                
            else:
                try:
                    # If received a command
                    data = sock.recv(1024);

                    if data: # and its data
                        newData = str(data);
                        print("Cliente PKey: "+newData); # print the public key received
                        # Send to all peers connecteds (less the owner of public key)
                        self.broadcast( self.server_socket, sock, "[UID]"+newData[2:-1]);
                    else: # if is not data, some trouble happens, so kill them
                        self.socket_list.remove(sock);
                except:
                    pass;