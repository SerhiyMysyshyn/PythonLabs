package com.example.aurafitv3.dialogs;

import android.app.Dialog;
import android.content.Context;
import android.content.SharedPreferences;
import android.media.MediaScannerConnection;
import android.os.Bundle;
import android.os.Environment;
import android.view.View;
import android.view.Window;
import android.view.WindowManager;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import com.example.aurafitv3.MainActivity;
import com.example.aurafitv3.picture.PickPhotoListActivity;
import com.example.aurafitv3.R;
import com.example.aurafitv3.RecyclerViews.ViewPhotoVerticalList.viewPhotoRecyclerViewAdapter;

import java.io.File;
import java.util.Vector;

public class RenamePictureDialog extends Dialog {

    public interface RenamePictureDialogListener {
        public void pictureNameEntered(String pictureName);
    }

    public Context context;
    private EditText pictureName_editText;
    private PickPhotoListActivity pickPhotoListActivity;
    private Button button_ok;
    private SharedPreferences preferencesData;
    private int position;
    private Vector<String> jpgFullPathsLcl;
    private File appliedFile;

    public RenamePictureDialog.RenamePictureDialogListener listener;

    public RenamePictureDialog(PickPhotoListActivity context,
                               RenamePictureDialog.RenamePictureDialogListener listener,
                               int position,
                               Vector<String> jpgFullPathsLcl,
                               File appliedFile) {
        super(context);
        pickPhotoListActivity = context;
        this.context = context;
        this.listener = listener;
        this.position = position;
        this.jpgFullPathsLcl = jpgFullPathsLcl;
        this.appliedFile = appliedFile;
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        View.OnFocusChangeListener listener = new View.OnFocusChangeListener() {
            @Override
            public void onFocusChange(View v, boolean hasFocus) {
                if (hasFocus) {
                    RenamePictureDialog.this.getWindow().setSoftInputMode(WindowManager.LayoutParams.SOFT_INPUT_STATE_ALWAYS_VISIBLE);
                }
            }
        };

        preferencesData = context.getSharedPreferences("aurafit", Context.MODE_PRIVATE);

        requestWindowFeature(Window.FEATURE_NO_TITLE);
        setContentView(R.layout.rename_picture_dialog);

        this.pictureName_editText = (EditText) findViewById(R.id.picture_name);
        this.button_ok = (Button) findViewById(R.id.picture_name_button_ok);

        this.button_ok.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String pictureNameString = pictureName_editText.getText().toString().trim();
                try {
                    boolean changeFile = false;
                    File file = new File(jpgFullPathsLcl.get(position));

                    String filePath = file.getAbsolutePath();
                    if (appliedFile != null && appliedFile.getName().equals(file.getName())) {
                        changeFile = true;
                    }
                    if (file.exists()) {
                        file.renameTo(new File(Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_PICTURES),"Aura iTrain V3" + File.separator + pictureNameString + ".jpg"));
                    } else {
                        System.out.println("file not exist");
                    }
                    MediaScannerConnection.scanFile(pickPhotoListActivity.getApplicationContext(), new String[]{filePath}, null, null);
                    if (changeFile) {
                        SharedPreferences.Editor editorLcl = preferencesData.edit();
                        editorLcl.putString("path", Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_PICTURES) + File.separator + "Aura iTrain V3" + File.separator + pictureNameString + ".jpg");
                        editorLcl.apply();
                        appliedFile = new File(Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_PICTURES), "Aura iTrain V3" + File.separator + pictureNameString + ".jpg");
                    }
                } catch (Exception e) {
                    e.printStackTrace();
                }
                cancel();
                pickPhotoListActivity.updateListState();
                Toast.makeText(getContext(), "Image name changed successfully", Toast.LENGTH_LONG).show();
            }
        });

    }

}
