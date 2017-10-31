package project.ds.transaction;

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.net.Socket;
import java.nio.ByteBuffer;
import java.sql.Connection;
import java.util.Calendar;
import java.util.UUID;
import java.util.logging.Logger;

import project.ds.transaction.database.DbUtil;

public class Dispatcher {
	private static final Logger LOGGER = Logger.getLogger(Dispatcher.class.getName());
	private static final int BUF_IN = 52;
	private static final int BUF_OUT = 17;
	private Socket socket;
	private DataInputStream in;
	private DataOutputStream out;
	
	public Dispatcher(Socket socket) throws IOException {
		this.socket = socket;
		in = new DataInputStream(socket.getInputStream());
		out = new DataOutputStream(socket.getOutputStream());
		out.flush();
		incoming();
	}
	
	protected void transaction(UUID tid, long time, float value, long giver, long receiver, long pKey) {
		Connection conn = DbUtil.getConnection();
		PeerDAO pDao = new PeerDAO(conn);
		Peer pGiver = pDao.find(giver);
		float giverBalance = pGiver.getBalance() - value;
		
		// In the future it will be validate() method
		if (pGiver.getSecurityKey() != pKey || giverBalance < 0) {
			ack(tid, false);
			DbUtil.closeConnection(conn);
			return;
		}
		
		ack(tid, true);
		
		// Commit
		Peer pReceiver = pDao.find(receiver);
		pReceiver.setBalance(pReceiver.getBalance() + value);
		pGiver.setBalance(giverBalance);
		
		TransactionDAO tDao = new TransactionDAO(conn);
		Transaction tx = new Transaction();
		Calendar cal = Calendar.getInstance();
		cal.setTimeInMillis(time);
		tx.setId(tid);
		tx.setDatetime(cal);
		tx.setGiver(pGiver);
		tx.setReceiver(pReceiver);
		tx.setValue(value);
		tDao.save(tx);
		DbUtil.closeConnection(conn);
	}
	
	protected void ack(UUID tid, boolean accepted) {
		byte buffer[] = new byte[BUF_OUT];
		ByteBuffer wrapped = ByteBuffer.wrap(buffer);
		wrapped.putLong(tid.getMostSignificantBits());
		wrapped.putLong(tid.getLeastSignificantBits());
		
		if (accepted) {
			LOGGER.info("Transaction tid:" + tid + " approved");
			wrapped.put((byte) 1);
		} else {
			LOGGER.info("Transaction tid:" + tid + " refused");
			wrapped.put((byte) 0);
		}
		
		try {
			out.write(buffer);
			out.close();
			in.close();
			socket.close();
		} catch (IOException e) {
			LOGGER.warning("Acknowledgement failure. tid: " + tid);
		}
	}
	
	private void incoming() throws IOException {
		byte buffer[] = new byte[BUF_IN];
		in.readFully(buffer, 0, BUF_IN);
		
		ByteBuffer wrapped = ByteBuffer.wrap(buffer);
		long htid = wrapped.getLong();
		long ltid = wrapped.getLong();
		long time = wrapped.getLong();
		float value = wrapped.getFloat();
		long giver = wrapped.getLong();
		long receiver = wrapped.getLong();
		long pKey = wrapped.getLong();
		UUID tid = new UUID(htid, ltid);
		
		LOGGER.info("Incoming transaction tid: " + tid);
		transaction(tid, time, value, giver, receiver, pKey);
	}
}