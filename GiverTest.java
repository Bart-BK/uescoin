package project.ds.transaction.test;

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.net.Socket;
import java.nio.ByteBuffer;
import java.util.UUID;

public class GiverTest {
	public static void main(String args[]) throws Exception {
		byte bufferIn[] = new byte[52];
		byte bufferOut[] = new byte[17];
		
		ByteBuffer wrapped = ByteBuffer.wrap(bufferIn);
		UUID uuid = UUID.randomUUID();
		wrapped.putLong(uuid.getMostSignificantBits());
		wrapped.putLong(uuid.getLeastSignificantBits());
		wrapped.putLong(System.currentTimeMillis());
		wrapped.putFloat(30.0f);
		wrapped.putLong(1L);
		wrapped.putLong(2L);
		wrapped.putLong(1L);
		
		Socket socket = new Socket("127.0.0.1", 45678);
		DataOutputStream out = new DataOutputStream(socket.getOutputStream());
		out.flush();
		DataInputStream in = new DataInputStream(socket.getInputStream());
		out.write(bufferIn);
		in.readFully(bufferIn, 0, 17);
		wrapped = ByteBuffer.wrap(bufferIn);
		long htid = wrapped.getLong();
		long ltid = wrapped.getLong();
		byte accepted = wrapped.get();
		
		uuid = new UUID(htid, ltid);
		System.out.println(uuid + " " + accepted);
		
		socket.close();
	}
}
