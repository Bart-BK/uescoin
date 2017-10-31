package project.ds.transaction;

import java.util.Calendar;
import java.util.UUID;

public class Transaction {	
	private UUID id;
	private float value;
	private Calendar time;
	private Peer giver;
	private Peer receiver;
	
	public UUID getId() {
		return id;
	}
	
	public float getValue() {
		return value;
	}
	
	public Calendar getTime() {
		return time;
	}
	
	public Peer getGiver() {
		return giver;
	}
	
	public Peer getReceiver() {
		return receiver;
	}
	
	public void setId(UUID id) {
		this.id = id;
	}
	
	public void setValue(float value) {
		this.value = value;
	}
	
	public void setDatetime(Calendar datetime) {
		this.time = datetime;
	}
	
	public void setGiver(Peer giver) {
		this.giver = giver;
	}
	
	public void setReceiver(Peer receiver) {
		this.receiver = receiver;
	}
}
