package org.ructf.ructfe2012.geotracker.push.client.order;

import org.apache.log4j.Logger;
import org.ructf.ructfe2012.geotracker.push.client.Client;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;

public class OrderClient extends Client implements IOrderClient {
	
	private Logger logger = Logger.getLogger(OrderClient.class);
	
	@Autowired
	@Value("${jury.secret}")
	String jury_secret;
	
	@Autowired
	IConnectionPool connections;
	
	@Override
	protected boolean readData(String data) {
		if (data == null) {
			return false;
		}
		data = data.trim();
		if (data.length() < 1) {
			logger.info("empty string");
			return false;
		}
		if (data.equals("lost")) {
			send("Is it easter Or iS it egg?\n");
			return true;
		}
		if (data.equals("IOS")) {
			send("Yep. What is it?\n");
			return true;
		}
		String[] request = data.split("\\s*\\|\\s*");
		if (request.length < 4) {
			send("Wrong request.\n");
			return true;
		}
		String secret = request[0];
		String teamIP = request[1];
		String client_id = request[2];
		String service_id = request[3];
		if (!secret.equals(jury_secret)) {
			send("Wrong secret.\n");
			return true;
		}
		connections.start(teamIP + client_id + service_id, teamIP, client_id, service_id);
		logger.info("threading " + teamIP + client_id + service_id);
		try {
			Thread.sleep(5000);
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
		send(connections.getPushes(teamIP + client_id + service_id) + "\n");
		
		return true;
	}

	@Override
	public String identifyClient() {
		return null;
	}

}
