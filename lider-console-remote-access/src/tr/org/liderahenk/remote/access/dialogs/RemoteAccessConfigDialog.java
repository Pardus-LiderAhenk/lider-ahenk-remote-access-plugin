package tr.org.liderahenk.remote.access.dialogs;

import org.eclipse.jface.dialogs.IDialogConstants;
import org.eclipse.jface.dialogs.TitleAreaDialog;
import org.eclipse.swt.SWT;
import org.eclipse.swt.events.SelectionEvent;
import org.eclipse.swt.events.SelectionListener;
import org.eclipse.swt.graphics.Image;
import org.eclipse.swt.layout.GridData;
import org.eclipse.swt.layout.GridLayout;
import org.eclipse.swt.widgets.Button;
import org.eclipse.swt.widgets.Composite;
import org.eclipse.swt.widgets.Control;
import org.eclipse.swt.widgets.Label;
import org.eclipse.swt.widgets.Shell;
import org.eclipse.swt.widgets.Text;

import tr.org.liderahenk.remote.access.i18n.Messages;

public class RemoteAccessConfigDialog extends TitleAreaDialog {

	private String ahenkDn;

	private Button btnConnect;
	private Text hostText;
	private Text portText;
	private Text passwordText;
	
	public RemoteAccessConfigDialog(Shell parentShell, String ahenkDn) {
		super(parentShell);
		this.ahenkDn = ahenkDn;
	}

	@Override
	protected Control createDialogArea(Composite parent) {

		Composite area = (Composite) super.createDialogArea(parent);
		Composite composite = new Composite(area, GridData.FILL);

		composite.setLayout(new GridLayout(2, false));
		composite.setLayoutData(new GridData(SWT.FILL, SWT.FILL, true, true));

		Label hostLabel = new Label(composite, SWT.NONE);
		hostLabel.setText(Messages.getString("REMOTE_HOST"));
		
		hostText = new Text(composite, SWT.NONE);
		hostText.setLayoutData(new GridData(SWT.FILL, SWT.FILL, true, false));
		hostText.setText("192.168.1.229");
		
		Label portlabel = new Label(composite, SWT.NONE);
		portlabel.setText(Messages.getString("PORT"));
		
		portText = new Text(composite, SWT.NONE);
		portText.setLayoutData(new GridData(SWT.FILL, SWT.FILL, true, false));
		portText.setText("5902");
		
		Label passwordlabel = new Label(composite, SWT.NONE);
		passwordlabel.setText(Messages.getString("PASSWORD"));
		
		passwordText = new Text(composite, SWT.PASSWORD);
		passwordText.setLayoutData(new GridData(SWT.FILL, SWT.FILL, true, false));
		passwordText.setText("mine5644");
		
		return composite;
	}

	@Override
	protected void createButtonsForButtonBar(Composite parent) {

		createButton(parent, IDialogConstants.CANCEL_ID, Messages.getString("CLOSE_BUTTON"), true);

		btnConnect = createButton(parent, 5000, Messages.getString("CONNECT_BUTTON"), false);
		btnConnect
				.setImage(new Image(parent.getDisplay(), this.getClass().getResourceAsStream("/icons/sample.png"))); // TODO icon bulunacak
		btnConnect.setText(Messages.getString("CONNECT_BUTTON"));
		
		btnConnect.addSelectionListener(new SelectionListener() {
			@Override
			public void widgetSelected(SelectionEvent e) {
				RemoteAccessConnection.invoke(hostText.getText(), portText.getText(), passwordText.getText());
			}

			@Override
			public void widgetDefaultSelected(SelectionEvent e) {
			}
		});
	}

	@Override
	public void create() {
		super.create();
		setTitle(Messages.getString("REMOTE_ACCESS_CONFIG"));
		setMessage(ahenkDn);
	}
}
