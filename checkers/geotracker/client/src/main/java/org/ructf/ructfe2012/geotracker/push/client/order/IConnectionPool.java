package org.ructf.ructfe2012.geotracker.push.client.order;

public interface IConnectionPool {

	void start(String key, String teamIP, String client_id, String service_id);

	String getPushes(String key);

}
