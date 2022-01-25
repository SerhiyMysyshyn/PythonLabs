package com.example.aurafitv3;

import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;

import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.SharedPreferences;
import android.content.res.Resources;
import android.os.Bundle;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import com.example.aurafitv3.camera.BackCameraActivity;
import com.example.aurafitv3.camera.FrontCameraActivity;
import com.example.aurafitv3.dialogs.InputUserNameDialog;
import com.example.aurafitv3.picture.PickPhotoFromGalleryActivity;
import com.example.aurafitv3.picture.PickPhotoListActivity;

import java.io.File;

public class MainActivity extends AppCompatActivity {

    private final static String TAG = "MainActivity";

    private static final int CONNECT = 0;
    private static final int TO_MAKE_SNAPSHOT = 50;

    ImageView backgroundImageView;
    private Resources res;
    private boolean isNameSet = false;
    private TextView tapToStart;
    private InputUserNameDialog inputUserNameDialog;
    private String touchSensortString, connectString, disconnectString, takeFacePhoto, takeFullPhoto, viewPhoto, choosePhotoFromGallery;

    protected boolean mConnected = false;

    private String path;

    private SharedPreferences preferencesData;

    private MenuItem connectMenuItem;
    private MenuItem mnuConnect, mnuMakeShot, mnuSetting;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        res = getResources();

        takeFacePhoto = res.getString(R.string.take_face_photo);
        takeFullPhoto = res.getString(R.string.take_full_photo);
        viewPhoto = res.getString(R.string.view_photo);
        choosePhotoFromGallery = res.getString(R.string.choose_photo_from_gallery);

        backgroundImageView = (ImageView)findViewById(R.id.background_image);
        tapToStart = (TextView) findViewById(R.id.tap_to_start);
        touchSensortString = res.getString(R.string.touch_sensor);
        connectString = res.getString(R.string.connect);
        disconnectString = res.getString(R.string.disconnect);

        preferencesData = getApplicationContext().getSharedPreferences("aurafit", Context.MODE_PRIVATE);
        //path = null;

        backgroundImageView.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if (view == null) {

                }
                if (isNameSet) {
                    //onOptionsItemSelected(mnuConnect);
                    /*System.out.println(">>> Name is already saved");
                    pause(1000);
                    System.out.println(">>> Connecting to smart watch");
                    pause(1000);
                    System.out.println(">>> Successfully connected!");*/

                    if (!mConnected){
                        mConnected = true;
                        showAuraActivity();
                    }else{
                        mConnected = false;
                        Toast.makeText(getApplicationContext(), "Disconnecting", Toast.LENGTH_SHORT).show();
                    }
                    invalidateOptionsMenu();

                } else {
                    alertUserName();
                    if (tapToStart != null) {
                        tapToStart.setText(touchSensortString != null ? touchSensortString : "");
                    }
                }
            }
        });
    }


    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.main, menu);

        //menu.removeItem(R.id.action_settings);

        try {
            mnuConnect = menu.add(0, CONNECT, 0, connectString);
            mnuConnect.setTitle(mConnected ? disconnectString : connectString);
            connectMenuItem = mnuConnect;

            mnuMakeShot = menu.add(0, TO_MAKE_SNAPSHOT, 3, getResources().getString(R.string.photos));
            mnuMakeShot.setTitle(getResources().getString(R.string.photos));
            mnuMakeShot.setVisible(!mConnected);

        }catch (Exception e){
            e.printStackTrace();
        }
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        switch (item.getItemId()){
            case CONNECT:
                // Перед конектом перевіряю, чи введене ім'я користувача
                if (!isNameSet) {
                    alertUserName();
                    if (tapToStart != null) {
                        tapToStart.setText(touchSensortString != null ? touchSensortString : "");
                    }
                    return false;
                }

                if (!mConnected){

                    Toast.makeText(getApplicationContext(), R.string.trying_message, Toast.LENGTH_SHORT).show();

                    showAuraActivity();

                    mConnected = true;
                }else{
                    mConnected = false;
                    Toast.makeText(getApplicationContext(), "Disconnecting", Toast.LENGTH_SHORT).show();
                }
                invalidateOptionsMenu();
                break;
            case TO_MAKE_SNAPSHOT:
                showPhotoOptionsDialog();
                break;
            case R.id.action_settings:
                String path = preferencesData.getString("path","");
                Toast.makeText(getApplicationContext(), path, Toast.LENGTH_SHORT).show();
                break;
        }
        return true;
    }

    public void showAuraActivity(){
        //check path to last snapshot
        System.out.println(">>> "+path);
        if (preferencesData.contains("path")) {
            path = preferencesData.getString("path", null);
        } else {
            path = null;
        }
        if (path != null) {
            File file = new File(path);
            //check whether file is there in the Picture/MyCameraApp directory
            if (!file.exists()) {
                SharedPreferences.Editor editor = preferencesData.edit();
                editor.putString("path", null);
                editor.apply();
            }
        }

        if (path != null){
            Intent intent = new Intent(MainActivity.this, ShowAura.class);
            intent.putExtra(ShowAura.IMGPATH, "file://"+path);
            startActivity(intent);
        }else{
            showPhotoOptionsDialog();
        }
    }

    private void showPhotoOptionsDialog(){
        final String[] photoParametersArray = {takeFacePhoto, takeFullPhoto, viewPhoto, choosePhotoFromGallery};

        AlertDialog.Builder builder = new AlertDialog.Builder(MainActivity.this);
        builder.setCancelable(true);
        builder.setItems(photoParametersArray, new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialogInterface, int i) {
                switch (i){
                    case 0:
                        Intent intent = new Intent(MainActivity.this, FrontCameraActivity.class);
                        startActivity(intent);
                        break;
                    case 1:
                        Intent intent2 = new Intent(MainActivity.this, BackCameraActivity.class);
                        startActivity(intent2);
                        break;
                    case 2:
                        Intent intent3 = new Intent(MainActivity.this, PickPhotoListActivity.class);
                        startActivity(intent3);
                        break;
                    case 3:
                        Intent intent4 = new Intent(MainActivity.this, PickPhotoFromGalleryActivity.class);
                        startActivity(intent4);
                        //Toast.makeText(getApplicationContext(), photoParametersArray[i], Toast.LENGTH_SHORT).show();
                        break;
                }
            }
        });

        AlertDialog alertDialog = builder.create();
        alertDialog.show();

    }

    private void alertUserName() {
        InputUserNameDialog.InputUserNameDialogListener listener = new InputUserNameDialog.InputUserNameDialogListener() {
            @Override
            public void userNameEntered(String userName) {
            }
        };
        inputUserNameDialog = new InputUserNameDialog(this, listener);
        inputUserNameDialog.show();
        }

    public void setIsPatientNameSet(boolean b) {
        isNameSet = b;
    }

    private void pause(long l) {
        try {
            Thread.sleep(l);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }

}