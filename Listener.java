package project.ds.transaction;

import java.io.IOException;
import java.net.ServerSocket;

public class Listener {
	public void start(int port) {
		try (ServerSocket serverSocket = new ServerSocket(port)) {
			new Dispatcher(serverSocket.accept());
			serverSocket.close();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
}
