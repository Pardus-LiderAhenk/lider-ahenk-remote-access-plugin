package tr.org.liderahenk.remote.access.handlers;

import org.eclipse.core.commands.AbstractHandler;
import org.eclipse.core.commands.ExecutionEvent;
import org.eclipse.core.commands.ExecutionException;
import org.eclipse.ui.IWorkbenchPage;
import org.eclipse.ui.IWorkbenchWindow;
import org.eclipse.ui.PartInitException;
import org.eclipse.ui.handlers.HandlerUtil;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import tr.org.liderahenk.remote.access.constants.RemoteAccessConstants;
import tr.org.liderahenk.remote.access.dialogs.RemoteAccessProfileDialog;
import tr.org.liderahenk.remote.access.i18n.Messages;
import tr.org.liderahenk.liderconsole.core.constants.LiderConstants;
import tr.org.liderahenk.liderconsole.core.editorinput.ProfileEditorInput;

public class RemoteAccessProfileHandler extends AbstractHandler {

	private Logger logger = LoggerFactory.getLogger(RemoteAccessProfileHandler.class);

	public Object execute(ExecutionEvent event) throws ExecutionException {
		
		IWorkbenchWindow window = HandlerUtil.getActiveWorkbenchWindowChecked(event);
        IWorkbenchPage page = window.getActivePage();
        
        try {
			page.openEditor(new ProfileEditorInput(Messages.getString("RemoteAccess"), RemoteAccessConstants.PLUGIN_NAME, 
					RemoteAccessConstants.PLUGIN_VERSION, new RemoteAccessProfileDialog()), 
					LiderConstants.EDITORS.PROFILE_EDITOR);
		} catch (PartInitException e) {
			logger.error(e.getMessage(), e);
		}

        return null;
	}

}
