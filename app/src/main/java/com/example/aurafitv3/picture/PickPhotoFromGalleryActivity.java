package com.example.aurafitv3.picture;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.drawable.BitmapDrawable;
import android.net.Uri;
import android.os.Bundle;
import android.os.Environment;
import android.provider.MediaStore;
import android.view.MotionEvent;
import android.view.View;
import android.view.WindowManager;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.widget.ImageView;
import android.widget.RelativeLayout;
import android.widget.TextView;
import android.widget.Toast;

import com.example.aurafitv3.R;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.Date;

public class PickPhotoFromGalleryActivity extends AppCompatActivity {

    private ImageView mask;
    private RelativeLayout relativeLayout;
    private String path;
    private Uri imageUri;
    private TextView selectPhoto, savePhoto;
    private WebView wv;
    private final int Pick_image = 1;
    private Bitmap selectedImage;
    private File file;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        getWindow().addFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN);
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_pick_photo_from_gallery);
        relativeLayout = (RelativeLayout)findViewById(R.id.rel);
        mask = (ImageView)findViewById(R.id.pre_face_mask);
        selectPhoto = (TextView)findViewById(R.id.selectPhoto_btn);
        savePhoto = (TextView)findViewById(R.id.savePhoto_btn);

        selectPhoto.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent photoPickerIntent = new Intent(Intent.ACTION_PICK);
                photoPickerIntent.setType("image/*");
                startActivityForResult(photoPickerIntent, Pick_image);
            }
        });

        savePhoto.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                mask.setVisibility(View.GONE);
                relativeLayout.setDrawingCacheEnabled(true);
                Bitmap bm = relativeLayout.getDrawingCache();
                BitmapDrawable bitmapDrawable = new BitmapDrawable(bm);

                File mediaStorageDir = new File(Environment.getExternalStoragePublicDirectory(
                        Environment.DIRECTORY_PICTURES), "Aura iTrain V3");

                if (!mediaStorageDir.exists()) {
                    File wallpaperDirectory = new File(Environment.getExternalStoragePublicDirectory(
                            Environment.DIRECTORY_PICTURES), "Aura iTrain V3");
                    wallpaperDirectory.mkdirs();
                }

                String timeStamp = "" + new Date().getTime();

                path = mediaStorageDir.getPath() + File.separator + timeStamp + ".jpg";
                File pictureFile = new File(path);
                try {
                    FileOutputStream fos = new FileOutputStream(pictureFile);
                    bm.compress(Bitmap.CompressFormat.PNG, 85, fos);
                    fos.close();
                    Toast.makeText(getApplicationContext(), "OK", Toast.LENGTH_SHORT).show();
                } catch (FileNotFoundException e) {
                    e.printStackTrace();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        });

        wv = (WebView) findViewById(R.id.pick_picture_from_gallery_view);
        wv.getSettings().setBuiltInZoomControls(true);
        WebSettings webSettings=wv.getSettings();
        webSettings.setUseWideViewPort(true);
        webSettings.setLoadWithOverviewMode(true);
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent imageReturnedIntent) {
        super.onActivityResult(requestCode, resultCode, imageReturnedIntent);

        switch(requestCode) {
            case Pick_image:
                if(resultCode == RESULT_OK){
                    try {
                        imageUri = imageReturnedIntent.getData();
                        file = new File(String.valueOf(imageUri));
                        final InputStream imageStream = getContentResolver().openInputStream(imageUri);
                        selectedImage = BitmapFactory.decodeStream(imageStream);
                        wv.loadUrl(String.valueOf(imageUri));

                    } catch (FileNotFoundException e) {
                        e.printStackTrace();
                    }
                }
        }
    }

}