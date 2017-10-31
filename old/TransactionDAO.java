dpackage project.ds.transaction;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;
import java.sql.Timestamp;
import java.util.Collection;

import project.ds.transaction.database.DAO;

public class TransactionDAO implements DAO<Transaction, Long> {
	private Connection conn;
	
	public TransactionDAO(Connection conn) {
		this.conn = conn;
	}
	
	@Override
	public void save(Transaction transaction) {
		String queryTransaction = "INSERT INTO tb_transaction VALUES (?, ?, ?, ?, ?, ?)";
		String queryPeer = "UPDATE tb_peer SET balance = ? WHERE pid = ?";
		Peer giver = transaction.getGiver();
		Peer receiver = transaction.getReceiver();
		
		try {
			boolean autoCommit = conn.getAutoCommit();
			conn.setAutoCommit(false);
			
			PreparedStatement pstm1 = conn.prepareStatement(queryTransaction);
			pstm1.setLong(1, transaction.getId().getMostSignificantBits());
			pstm1.setLong(2, transaction.getId().getLeastSignificantBits());
			Timestamp time = new Timestamp(transaction.getTime().getTimeInMillis());
			pstm1.setTimestamp(3, time);
			pstm1.setFloat(4, transaction.getValue());
			pstm1.setLong(5, giver.getId());
			pstm1.setLong(6, receiver.getId());
			pstm1.execute();
			
			PreparedStatement pstm2 = conn.prepareStatement(queryPeer);
			pstm2.setFloat(1, giver.getBalance());
			pstm2.setLong(2, giver.getId());
			pstm2.execute();
			
			PreparedStatement pstm3 = conn.prepareStatement(queryPeer);
			pstm3.setFloat(1, receiver.getBalance());
			pstm3.setLong(2, receiver.getId());
			pstm3.execute();
			
			conn.commit();
			conn.setAutoCommit(autoCommit);
		} catch (SQLException e) {
			// Rollback goes here
			throw new RuntimeException(e);
		}
	}

	@Override
	public void update(Transaction obj) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public Transaction find(Long key) {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public Collection<Transaction> findAll() {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public void delete(Transaction obj) {
		// TODO Auto-generated method stub
		
	}
}
