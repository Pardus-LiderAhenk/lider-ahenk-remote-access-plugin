package tr.org.liderahenk.remote.access.handlers;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import org.codehaus.jackson.map.ObjectMapper;
import org.eclipse.core.runtime.IProgressMonitor;
import org.eclipse.core.runtime.IStatus;
import org.eclipse.core.runtime.Status;
import org.eclipse.core.runtime.jobs.Job;
import org.eclipse.e4.core.services.events.IEventBroker;
import org.eclipse.ui.PlatformUI;
import org.osgi.service.event.Event;
import org.osgi.service.event.EventHandler;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import tr.org.liderahenk.liderconsole.core.constants.LiderConstants;
import tr.org.liderahenk.liderconsole.core.handlers.SingleSelectionHandler;
import tr.org.liderahenk.liderconsole.core.model.TaskStatus;
import tr.org.liderahenk.liderconsole.core.rest.enums.RestDNType;
import tr.org.liderahenk.liderconsole.core.rest.requests.TaskRequest;
import tr.org.liderahenk.liderconsole.core.rest.utils.TaskUtils;
import tr.org.liderahenk.liderconsole.core.widgets.Notifier;
import tr.org.liderahenk.remote.access.constants.RemoteAccessConstants;
import tr.org.liderahenk.remote.access.i18n.Messages;
import tr.org.liderahenk.remote.access.listeners.RemoteAccessConnection;

public class RemoteAccessTaskHandler extends SingleSelectionHandler {

	private static final Logger logger = LoggerFactory.getLogger(RemoteAccessTaskHandler.class);

	private IEventBroker eventBroker = (IEventBroker) PlatformUI.getWorkbench().getService(IEventBroker.class);

	@Override
	public void executeWithDn(String dn) {

		// TODO improvement. (after XMPPClient fix) Instead of 'TASK' topic use
		// plugin name as event topic
		eventBroker.subscribe(LiderConstants.EVENT_TOPICS.TASK, eventHandler);

		// Create task request
		TaskRequest request = new TaskRequest();
		request.setCommandId("SETUP-VNC-SERVER");
		request.setPluginName(RemoteAccessConstants.PLUGIN_NAME);
		request.setPluginVersion(RemoteAccessConstants.PLUGIN_VERSION);
		List<String> dnList = new ArrayList<String>();
		dnList.add(dn);
		request.setDnList(dnList);
		request.setDnType(RestDNType.AHENK);

		try {
			// DO NOT connect to VNC here! First send this task to let
			// agent to install/configure VNC server.
			// (VNC connection is handled inside EventHandler class
			// below!)
			TaskUtils.execute(request);
		} catch (Exception e1) {
			logger.error(e1.getMessage(), e1);
			Notifier.error(null, Messages.getString("ERROR_ON_EXECUTE"));
		}

	}

	private EventHandler eventHandler = new EventHandler() {
		@Override
		public void handleEvent(final Event event) {
			Job job = new Job("TASK") {
				@Override
				protected IStatus run(IProgressMonitor monitor) {

					monitor.beginTask("VNC", 100);

					try {

						String body = (String) event.getProperty("org.eclipse.e4.data");
						TaskStatus taskStatus = new ObjectMapper().readValue(body, TaskStatus.class);
						Map<String, Object> responseData = taskStatus.getResponseData();

						// Host may have contain multiple IP addresses
						String[] ipAddresses = ((String) responseData.get("host")).split(",");
						for (int i = 0; i < ipAddresses.length; i++) {
							String ipAddress = ipAddresses[i];
							try {
								// Try to connect VNC via
								// {ipAddress,port,password}
								// provided from agent itself.
								RemoteAccessConnection.invoke(ipAddress, (String) responseData.get("port"),
										(String) responseData.get("password"));
							} catch (Exception e) {
								logger.error(e.getMessage(), e);
								if (i == ipAddresses.length - 1) {
									Notifier.error("", Messages.getString("COULD_NOT_CONNECT_VNC"));
								} else {
									Notifier.error("", Messages.getString("COULD_NOT_CONNECT_VNC_TRY_ANOTHER"));
								}
							}
						}

					} catch (Exception e) {
						logger.error(e.getMessage(), e);
						Notifier.error("", Messages.getString("UNEXPECTED_ERROR_CONNECTING_VNC"));
					}

					monitor.worked(100);
					monitor.done();

					return Status.OK_STATUS;
				}
			};

			job.setUser(true);
			job.schedule();
		}
	};

	@Override
	public void dispose() {
		super.dispose();
		eventBroker.unsubscribe(eventHandler);
	}

}
