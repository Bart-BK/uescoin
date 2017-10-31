package project.ds.transaction.database;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class DbUtil {
	private static String url;

	public static void setProperties(String host, int port, String database, String user, String password) {
		url = "jdbc:mysql://" + host + ":" + port + "/" + database + "?user=" + user + "&password=" + password
				+ "&useSSL=false";
	}

	public static Connection getConnection() {
		Connection conn;

		try {
			conn = DriverManager.getConnection(url);
		} catch (SQLException e) {
			throw new RuntimeException(e);
		}

		return conn;
	}
	
	public static void closeConnection(Connection conn) {
		try {
			conn.close();
		} catch (SQLException e) {
			throw new RuntimeException(e);
		}
	}
}
