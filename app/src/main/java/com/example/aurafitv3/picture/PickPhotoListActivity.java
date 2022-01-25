package com.example.aurafitv3.picture;

import androidx.appcompat.app.ActionBar;
import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.SharedPreferences;
import android.content.res.Resources;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.drawable.BitmapDrawable;
import android.graphics.drawable.Drawable;
import android.media.MediaScannerConnection;
import android.net.Uri;
import android.os.Bundle;
import android.os.Environment;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.ProgressBar;
import android.widget.ScrollView;
import android.widget.TextView;


import com.example.aurafitv3.R;
import com.example.aurafitv3.RecyclerViews.SingleModeHorizontalList.horizontalRecyclerViewClickListener;
import com.example.aurafitv3.RecyclerViews.ViewPhotoVerticalList.viewPhotoRecyclerViewAdapter;
import com.example.aurafitv3.ShowAura;
import com.example.aurafitv3.camera.BackCameraActivity;
import com.example.aurafitv3.camera.FrontCameraActivity;
import com.example.aurafitv3.dialogs.RenamePictureDialog;

import java.io.File;
import java.util.Arrays;
import java.util.Comparator;
import java.util.HashMap;
import java.util.Vector;

public class PickPhotoListActivity extends AppCompatActivity {
    TextView takePhoto, empyListHint, selectItemHint, empyListHint2;
    ScrollView mScrollView;
    ProgressBar progressBar;

    private SharedPreferences preferencesData;
    private Resources res;
    private File appliedFile;
    private String imagesDirectoryLcl;
    private Vector<String> jpgFullPathsLcl;
    private HashMap<Integer, Drawable> data;
    private File file;
    private File[] jpgPathsArrayLcl;
    private LinearLayoutManager verticalLayoutManager;
    private RecyclerView recyclerView;
    private viewPhotoRecyclerViewAdapter adapter;

    private RenamePictureDialog renamePictureDialog;

    private String takeFacePhoto, takeFullPhoto,
            str_apply, str_view, str_rename, str_delete;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_pick_photo_list);
        ActionBar actionBar = getSupportActionBar();
        actionBar.setHomeButtonEnabled(true);
        actionBar.setDisplayHomeAsUpEnabled(true);

        res = this.getResources();
        preferencesData = getApplicationContext().getSharedPreferences("aurafit", Context.MODE_PRIVATE);

        progressBar = (ProgressBar)findViewById(R.id.progressBar);
        progressBar.setVisibility(View.VISIBLE);

        takeFacePhoto = res.getString(R.string.take_face_photo);
        takeFullPhoto = res.getString(R.string.take_full_photo);

        str_apply = res.getString(R.string.apply_str);
        str_view = res.getString(R.string.view_str);
        str_rename = res.getString(R.string.rename_str);
        str_delete = res.getString(R.string.del_str);

        takePhoto = (TextView)findViewById(R.id.button_take_photo);
        mScrollView = (ScrollView)findViewById(R.id.pick_photo_sv);
        empyListHint = (TextView)findViewById(R.id.textView2);
        selectItemHint = (TextView)findViewById(R.id.textView_hint);
        empyListHint2 = (TextView)findViewById(R.id.textView_empty);

        recyclerView = findViewById(R.id.view_photo_rv);
        verticalLayoutManager = new LinearLayoutManager(PickPhotoListActivity.this, LinearLayoutManager.VERTICAL, false);
        recyclerView.setLayoutManager(verticalLayoutManager);

        imagesDirectoryLcl = Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_PICTURES) + File.separator + "Aura iTrain V3";

        if (preferencesData.contains("path")) {
            String path = preferencesData.getString("path", null);
            if (path != null) {
                try {
                    appliedFile = new File(path);
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        }

        try {
            imagesDirectoryLcl = file.getCanonicalPath();
        }catch (Exception e){
            System.out.println("Error: "+e);
        }
        file = new File(imagesDirectoryLcl);
        if (file == null) return;
        jpgPathsArrayLcl = file.listFiles();

// Creating RecyclerView
        createRecyclerView(file, jpgPathsArrayLcl, data);

        takePhoto.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                showPhotoOptionsDialog();
            }
        });

        recyclerView.addOnItemTouchListener(new horizontalRecyclerViewClickListener(this, new horizontalRecyclerViewClickListener.OnItemClickListener() {
            @Override
            public void onItemClick(View view, int position) {
                String img_path = /*"file://" + */jpgFullPathsLcl.get(position);
                actionsWithPictureDialog(img_path, position);
            }
        }));

    }

// Picture -----------------------------------------------------------------------------------------
    private void renamePicture(int p){
        RenamePictureDialog.RenamePictureDialogListener listener = new RenamePictureDialog.RenamePictureDialogListener() {
            @Override
            public void pictureNameEntered(String pictureName) {
            }
        };
        renamePictureDialog = new RenamePictureDialog(PickPhotoListActivity.this, listener, p, jpgFullPathsLcl, appliedFile);
        renamePictureDialog.show();
    }

    private void deletePicture(int p){
        try {
            File curret_file = new File(jpgFullPathsLcl.get(p));
            Uri uri = Uri.fromFile(curret_file);
            String filePath = curret_file.getAbsolutePath();
            if (appliedFile != null && appliedFile.getName().equals(curret_file.getName())) {
                SharedPreferences.Editor editor = preferencesData.edit();
                editor.remove("path");
                editor.apply();
            }
            if (curret_file.exists()) {
                if (curret_file.delete()) {
                    System.out.println("file Deleted");
                } else {
                    System.out.println("file not Deleted");
                }
                try {
                    getContentResolver().delete(uri, null, null);
                } catch (Exception e) {
                    e.printStackTrace();
                }
            } else {
                System.out.println("file not exist");
            }
            MediaScannerConnection.scanFile(getApplicationContext(), new String[]{filePath}, null, null);
            createRecyclerView(file, file.listFiles(), data);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

// RecyclerView ------------------------------------------------------------------------------------
    private void createRecyclerView(File f, File[] jpgPathsArr, HashMap<Integer, Drawable> itemData) {
        if(!f.exists() || jpgPathsArr.length == 0){
            mScrollView.setVisibility(View.GONE);
            selectItemHint.setVisibility(View.GONE);
            progressBar.setVisibility(View.GONE);
            empyListHint2.setVisibility(View.VISIBLE);
            takePhoto.setVisibility(View.VISIBLE);
            empyListHint.setVisibility(View.VISIBLE);
        }else{
            mScrollView.setVisibility(View.VISIBLE);
            selectItemHint.setVisibility(View.VISIBLE);

            empyListHint2.setVisibility(View.GONE);
            takePhoto.setVisibility(View.GONE);
            empyListHint.setVisibility(View.GONE);

            new Thread(new Runnable() {
                @Override
                public void run() {
                    Arrays.sort(jpgPathsArr, new Comparator<File>() {
                        public int compare(File f1, File f2) {
                            return -(Long.valueOf(f1.lastModified()).compareTo(f2.lastModified()));
                        }
                    });

                    jpgFullPathsLcl = new Vector<String>();
                    for (File file : jpgPathsArr) {
                        if (file.getName().toLowerCase().contains(".jpg"))
                            jpgFullPathsLcl.add(imagesDirectoryLcl + File.separator + file.getName());
                    }

                    Vector<Drawable> drawablesLcl = new Vector<Drawable>();
                    int iconSideLcl;
                    Bitmap bitmap = null;
                    int height = PickPhotoListActivity.this.getWindowManager().getDefaultDisplay().getHeight();
                    iconSideLcl = height / 4;
                    for (String s : jpgFullPathsLcl) {
                        bitmap = BitmapFactory.decodeFile(s);
                        if (bitmap == null)
                            continue;
                        bitmap = Bitmap.createScaledBitmap(bitmap, iconSideLcl, iconSideLcl, true);
                        drawablesLcl.add(new BitmapDrawable(res, bitmap));
                    }

                    data = new HashMap<>();
                    for (int i = 0; i < drawablesLcl.size(); i++) {
                        data.put(i, drawablesLcl.get(i));
                    }

                    adapter = new viewPhotoRecyclerViewAdapter(data, jpgPathsArr, PickPhotoListActivity.this);
                    PickPhotoListActivity.this.runOnUiThread(new Runnable() {
                        public void run() {
                            progressBar.setVisibility(View.GONE);
                            recyclerView.setAdapter(adapter);
                        }
                    });
                }
            }).start();
        }
    }

    public void updateListState(){
        imagesDirectoryLcl = Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_PICTURES) + File.separator + "Aura iTrain V3";
        try {
            imagesDirectoryLcl = file.getCanonicalPath();
        }catch (Exception e){
            System.out.println("Error: "+e);
        }
        file = new File(imagesDirectoryLcl);
        if (file == null) return;
        jpgPathsArrayLcl = file.listFiles();

        createRecyclerView(file, jpgPathsArrayLcl, data);
    }

// Dialogs -----------------------------------------------------------------------------------------
    private void showPhotoOptionsDialog(){
        final String[] photoParametersArray = {takeFacePhoto, takeFullPhoto};

        AlertDialog.Builder builder = new AlertDialog.Builder(PickPhotoListActivity.this);
        builder.setCancelable(true);
        builder.setItems(photoParametersArray, new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialogInterface, int i) {
                switch (i){
                    case 0:
                        Intent intent = new Intent(PickPhotoListActivity.this, FrontCameraActivity.class);
                        startActivity(intent);
                        break;
                    case 1:
                        Intent intent2 = new Intent(PickPhotoListActivity.this, BackCameraActivity.class);
                        startActivity(intent2);
                        break;
                }
            }
        });
        AlertDialog alertDialog = builder.create();
        alertDialog.show();
    }

    private void actionsWithPictureDialog(String path, int pos){
        final String[] photoParametersArray = {str_apply, str_view, str_rename, str_delete};

        AlertDialog.Builder builder = new AlertDialog.Builder(PickPhotoListActivity.this);
        builder.setCancelable(true);
        builder.setItems(photoParametersArray, new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialogInterface, int i) {
                switch (i){
                    case 0:
                        SharedPreferences.Editor editorLcl = preferencesData.edit();
                        editorLcl.putString("path", path);
                        editorLcl.apply();
                        finish();
                        break;
                    case 1:
                        Intent photoPickerIntent = new Intent(PickPhotoListActivity.this, ShowAura.class);
                        photoPickerIntent.putExtra(ShowAura.IMGPATH, "file://"+path);
                        startActivity(photoPickerIntent);
                        break;
                    case 2:
                        renamePicture(pos);
                        break;
                    case 3:
                        deletePicture(pos);
                        break;
                }
            }
        });
        AlertDialog alertDialog = builder.create();
        alertDialog.show();
    }

// Button goBack -----------------------------------------------------------------------------------
    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        switch (item.getItemId()) {
            case android.R.id.home:
                this.finish();
                return true;
            case R.id.action_take_picture:
                showPhotoOptionsDialog();
                break;
        }
        return true;
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.take_picture, menu);
        return true;
    }



// Lifecycle ---------------------------------------------------------------------------------------
    @Override
    protected void onRestart(){
        super.onRestart();
        imagesDirectoryLcl = Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_PICTURES) + File.separator + "Aura iTrain V3";
        try {
            imagesDirectoryLcl = file.getCanonicalPath();
        }catch (Exception e){
            System.out.println("Error: "+e);
        }
        file = new File(imagesDirectoryLcl);
        if (file == null) return;
        jpgPathsArrayLcl = file.listFiles();

        createRecyclerView(file, jpgPathsArrayLcl, data);
    }


}