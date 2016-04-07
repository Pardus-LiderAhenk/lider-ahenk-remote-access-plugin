package tr.org.liderahenk.remote.access.plugininfo;

import tr.org.liderahenk.lider.core.api.plugin.IPluginInfo;

public class PluginInfoImpl implements IPluginInfo {
	
	@Override
	public String getPluginName() {
		return "remote-access";
	}

	@Override
	public String getPluginVersion() {
		return "1.0.0";
	}

	@Override
	public String getDescription() {
		return "Lider Remote Access (VNC) Plugin";
	}

	@Override
	public boolean isMachineOriented() {
		return true;
	}

	@Override
	public boolean isUserOriented() {
		return false;
	}

	@Override
	public boolean isPolicyPlugin() {
		return false;
	}

	@Override
	public boolean isxBased() {
		return false;
	}
	
}
