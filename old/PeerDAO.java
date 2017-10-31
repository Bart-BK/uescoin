package project.ds.transaction;

import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.Collection;

import project.ds.transaction.database.DAO;

public class PeerDAO implements DAO<Peer, Long> {
	private Connection conn;
	
	public PeerDAO(Connection conn) {
		this.conn = conn;
	}
	
	@Override
	public void save(Peer peer) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void update(Peer peer) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public Peer find(Long id) {
		Peer peer = null;
		String query = "SELECT * FROM tb_peer WHERE pid = " + id;
		
		try {
			ResultSet result = conn.createStatement().executeQuery(query);
			result.next();
			peer = new Peer();
			peer.setId(result.getLong("pid"));
			peer.setBalance(result.getFloat("balance"));
			peer.setSecurityKey(result.getLong("pkey"));
		} catch (SQLException e) {
			throw new RuntimeException(e);
		}
		
		return peer;
	}

	@Override
	public Collection<Peer> findAll() {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public void delete(Peer obj) {
		// TODO Auto-generated method stub
		
	}

}
