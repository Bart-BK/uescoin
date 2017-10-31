package project.ds.transaction;

public class Peer {
	private long id;
	private long securityKey;
	private float balance;
	
	public long getId() {
		return id;
	}
	
	public long getSecurityKey() {
		return securityKey;
	}
	
	public float getBalance() {
		return balance;
	}
	
	public void setId(long id) {
		this.id = id;
	}
	
	public void setSecurityKey(long securityKey) {
		this.securityKey = securityKey;
	}
	
	public void setBalance(float balance) {
		this.balance = balance;
	}
	
	@Override
	public String toString() {
		return id + " " + balance + " " + securityKey; 
	}
}