package com.example.aurafitv3;

import androidx.appcompat.app.ActionBar;
import androidx.appcompat.app.AppCompatActivity;

import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.drawable.Drawable;
import android.net.Uri;
import android.os.Bundle;
import android.view.MenuItem;
import android.view.Window;
import android.view.WindowManager;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.widget.ImageView;
import android.widget.Toast;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;

public class ShowAura extends AppCompatActivity {

    public final static String IMGPATH = "IMGPATH";
    private String path;
    private Bitmap bitmap;

    protected void onCreate(Bundle savedInstanceState) {

        getWindow().addFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN);
        //requestWindowFeature(Window.FEATURE_NO_TITLE);

        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_show_aura);
        ActionBar actionBar = getSupportActionBar();
        actionBar.setHomeButtonEnabled(true);
        actionBar.setDisplayHomeAsUpEnabled(true);

        ImageView imageView = (ImageView) findViewById(R.id.picture_view);

        String extras = getIntent().getStringExtra(IMGPATH);
        if(extras !=null) {
            path=extras;
        }

        try {
            InputStream is = getContentResolver().openInputStream(Uri.parse(path));
            bitmap = BitmapFactory.decodeStream(is);
            imageView.setImageBitmap(bitmap);
            is.close();
        } catch (IOException e) {
            e.printStackTrace();
        }






        /*WebView wv = (WebView) findViewById(R.id.picture_view);
        wv.getSettings().setBuiltInZoomControls(true);
        WebSettings webSettings=wv.getSettings();
        webSettings.setUseWideViewPort(true);
        webSettings.setLoadWithOverviewMode(true);
        wv.loadUrl(path);
        Toast.makeText(getApplicationContext(), path, Toast.LENGTH_SHORT).show();*/

    }


    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        switch (item.getItemId()) {
            case android.R.id.home:
                this.finish();
                return true;
        }
        return true;
    }
}