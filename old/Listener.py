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

            else:
                try:
                    # If received a command
                    data = sock.recv(1024);

                    if data: # and its data
                        newData = str(data);
                    else: # if is not data, some trouble happens, so kill them
                        self.socket_list.remove(sock);
                except:
                    pass;
