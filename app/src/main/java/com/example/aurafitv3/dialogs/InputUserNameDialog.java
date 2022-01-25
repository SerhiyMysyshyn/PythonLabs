package com.example.aurafitv3.dialogs;

import android.app.Dialog;
import android.content.Context;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.view.View;
import android.view.Window;
import android.view.WindowManager;
import android.widget.Button;
import android.widget.EditText;

import com.example.aurafitv3.MainActivity;
import com.example.aurafitv3.R;

public class InputUserNameDialog extends Dialog {

    public interface InputUserNameDialogListener {
        public void userNameEntered(String userName);
    }

    public Context context;
    private EditText username_editText;
    private MainActivity mainActivity;
    private Button button_ok;
    private SharedPreferences preferencesData;
    private String userName;


    public InputUserNameDialog.InputUserNameDialogListener listener;

    public InputUserNameDialog(MainActivity context, InputUserNameDialog.InputUserNameDialogListener listener) {
        super(context);
        mainActivity = context;
        this.context = context;
        this.listener = listener;
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);


        View.OnFocusChangeListener listener = new View.OnFocusChangeListener() {
            @Override
            public void onFocusChange(View v, boolean hasFocus) {
                if (hasFocus) {
                    InputUserNameDialog.this.getWindow().setSoftInputMode(WindowManager
                            .LayoutParams.SOFT_INPUT_STATE_ALWAYS_VISIBLE);
                }
            }
        };

        preferencesData = context.getSharedPreferences("aurafit", Context.MODE_PRIVATE);

        requestWindowFeature(Window.FEATURE_NO_TITLE);
        setContentView(R.layout.tap_to_start_dialog);

        this.username_editText = (EditText) findViewById(R.id.username);
        this.button_ok = (Button) findViewById(R.id.username_button_ok);
        this.setCancelable(false);

        userName = preferencesData.getString("user_name_1","");

        if (userName.length() > 0 && mainActivity != null) mainActivity.setIsPatientNameSet(true);
        username_editText.setText(userName);

        this.button_ok.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String userString = username_editText.getText().toString().trim();
                if (userString.length() > 0) {
                    if (mainActivity != null) mainActivity.setIsPatientNameSet(true);

                    SharedPreferences.Editor editorLcl = preferencesData.edit();
                    editorLcl.putString("user_name_1", userString);
                    editorLcl.apply();
                    cancel();
                }
            }
        });

    }

}
