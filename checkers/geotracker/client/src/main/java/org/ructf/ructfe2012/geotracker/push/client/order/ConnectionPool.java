package org.ructf.ructfe2012.geotracker.push.client.order;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;

import org.apache.log4j.Logger;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import org.springframework.util.StringUtils;

@Component
public class ConnectionPool implements IConnectionPool {

	private Logger logger = Logger.getLogger(ConnectionPool.class);

	@Autowired
	@Value("${push.port}")
	int push;

	protected Map<String, List<String>> pushes = new HashMap<String, List<String>>();

	@Override
	public void start(final String key, final String teamIP,
			final String client_id, final String service_id) {
		try {
			Socket s = new Socket(teamIP, push);
			PrintWriter out = new PrintWriter(s.getOutputStream(), true);
			out.print(client_id + ":0:" + service_id + "\n");
			BufferedReader in = new BufferedReader(new InputStreamReader(
					s.getInputStream()));
			String res = in.readLine();
			synchronized (pushes) {
				if (!pushes.containsKey(key)) {
					pushes.put(key, new LinkedList<String>());
				}
				pushes.get(key).add(res);
			}
		} catch (Exception e) {
			logger.error("error", e);
		}
	}

	@Override
	public String getPushes(String key) {
		synchronized (pushes) {
			if (pushes.containsKey(key) && pushes.get(key).size() > 0) {
				logger.info("have any pushes for " + key);
				return StringUtils.arrayToDelimitedString(pushes.get(key)
						.toArray(), "|");
			}
			logger.info("have no pushes for " + key);
			return "empty";
		}
	}

}
