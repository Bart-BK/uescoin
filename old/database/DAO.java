package project.ds.transaction.database;

import java.util.Collection;

public interface DAO<T, K> {
	public void save(T obj);
	public void update(T obj);
	public T find(K key);
	public Collection<T> findAll();
	public void delete(T obj);
}
