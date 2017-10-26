package project.ds.transaction.test;

import project.ds.transaction.Listener;
import project.ds.transaction.database.DbUtil;

public class ReceiverTest {
	public static void main(String args[]) {
		DbUtil.setProperties("localhost", 3306, "db_p2p_transaction", "root", "12345");
		new Listener().start(45678);
	}
}
