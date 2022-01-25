package com.example.aurafitv3.camera;

import androidx.appcompat.app.AppCompatActivity;

import android.app.Activity;
import android.app.ProgressDialog;
import android.content.Context;
import android.content.SharedPreferences;
import android.content.pm.ActivityInfo;
import android.content.res.Configuration;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Canvas;
import android.graphics.Matrix;
import android.graphics.Point;
import android.graphics.RectF;
import android.hardware.Camera;
import android.media.ExifInterface;
import android.os.Build;
import android.os.Bundle;
import android.os.Environment;
import android.util.TypedValue;
import android.view.Display;
import android.view.SurfaceHolder;
import android.view.SurfaceView;
import android.view.View;
import android.view.ViewGroup;
import android.view.Window;
import android.view.WindowManager;
import android.widget.Button;

import com.example.aurafitv3.R;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.Date;

public class FrontCameraActivity extends Activity implements SurfaceHolder.Callback, View.OnClickListener, Camera.PreviewCallback, Camera.AutoFocusCallback {

    private Camera camera;
    private SurfaceHolder surfaceHolderFront;
    private SurfaceView preview;
    private Button shotBtn;
    private ProgressDialog mProgressDialog;
    private FunctionsForPicture functionsForPicture = new FunctionsForPicture();
    private String path;
    private int width;
    private int height;
    private SharedPreferences preferencesData;
    protected Bitmap realImage;
    protected Bitmap newBitmap;
    private boolean imageSaved = false;
    final int version = android.os.Build.VERSION.SDK_INT;

    public static final int JPG_TYPE_IMAGE = 1;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_USER_PORTRAIT);
        getWindow().addFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN);
        requestWindowFeature(Window.FEATURE_NO_TITLE);

        setContentView(R.layout.activity_front_camera);

        preview = (SurfaceView) findViewById(R.id.front_camera_view);

        surfaceHolderFront = preview.getHolder();
        surfaceHolderFront.addCallback(this);
        surfaceHolderFront.setType(SurfaceHolder.SURFACE_TYPE_PUSH_BUFFERS);

        shotBtn = (Button) findViewById(R.id.button_front_snapshot);
        shotBtn.setOnClickListener(this);


        Display display = getWindowManager().getDefaultDisplay();
        if (version >= Build.VERSION_CODES.LOLLIPOP) {
            Point size = new Point();
            display.getSize(size);
            width = size.x;
            height = size.y;
        } else {
            width = display.getWidth();
            height = display.getHeight();
        }
    }

    @Override
    protected void onResume() {
        super.onResume();
            camera = Camera.open(Camera.CameraInfo.CAMERA_FACING_FRONT);
    }

    @Override
    protected void onPause() {
        super.onPause();
        if (camera != null) {
            camera.setPreviewCallback(null);
            camera.stopPreview();
            camera.release();
            camera = null;
        }
    }

    @Override
    public void surfaceChanged(SurfaceHolder holder, int format, int width, int height) {
    }

    @Override
    public void surfaceCreated(SurfaceHolder holder) {
        try {
            camera.setPreviewDisplay(holder);
            camera.setPreviewCallback(this);
        }
        catch (IOException e) {
            e.printStackTrace();
        }

        Camera.Size previewSize = camera.getParameters().getPreviewSize();
        float aspect = (float) previewSize.width / previewSize.height;

        int previewSurfaceWidth = preview.getWidth();
        int previewSurfaceHeight = preview.getHeight();

        ViewGroup.LayoutParams lp = preview.getLayoutParams();

        if (this.getResources().getConfiguration().orientation != Configuration.ORIENTATION_LANDSCAPE) {
            camera.setDisplayOrientation(90);
            lp.height = previewSurfaceHeight;
            lp.width = (int) (previewSurfaceHeight / aspect);
        }
        else {
            camera.setDisplayOrientation(0);
            lp.width = previewSurfaceWidth;
            lp.height = (int) (previewSurfaceWidth / aspect);
        }

        preview.setLayoutParams(lp);
        camera.startPreview();
    }

    @Override
    public void surfaceDestroyed(SurfaceHolder holder) {}

    @Override
    public void onClick(View v) {
        if (v == shotBtn) {
            new Thread(new Runnable() {
                public void run() {
                    camera.takePicture(null, null, null, mPicture);
                }
            }).start();

            mProgressDialog = new ProgressDialog(FrontCameraActivity.this);
            mProgressDialog.setMessage("Aura photo is being created...");
            mProgressDialog.setCanceledOnTouchOutside(false);
            mProgressDialog.setIndeterminate(true);
            mProgressDialog.show();

        }
    }

    private Camera.PictureCallback mPicture = new Camera.PictureCallback() {

        @Override
        public void onPictureTaken(byte[] paramArrayOfByte, Camera camera) {

            File pictureFile = functionsForPicture.getOutputMediaFile(JPG_TYPE_IMAGE, getApplicationContext());
            if (pictureFile == null) {
                System.out.println("Error creating media file, check storage permissions: ");
                return;
            }

            if (pictureFile.exists()) {
                pictureFile.delete();
            }

            android.hardware.Camera.CameraInfo info = new android.hardware.Camera.CameraInfo();
            android.hardware.Camera.getCameraInfo(1, info);

            try {
                FileOutputStream fos = new FileOutputStream(pictureFile);
                BitmapFactory.Options optionsLcl = new BitmapFactory.Options();
                optionsLcl.inPurgeable = true;
                realImage = BitmapFactory.decodeByteArray(paramArrayOfByte, 0, paramArrayOfByte.length, optionsLcl);
                ExifInterface exif = new ExifInterface(pictureFile.toString());

                if (exif.getAttribute(ExifInterface.TAG_ORIENTATION).equalsIgnoreCase("6")) {
                    realImage = functionsForPicture.rotateBitmap(realImage, 270 % 360);
                } else if (exif.getAttribute(ExifInterface.TAG_ORIENTATION).equalsIgnoreCase("8")) {
                    realImage = functionsForPicture.rotateBitmap(realImage, 90 % 360);
                } else if (exif.getAttribute(ExifInterface.TAG_ORIENTATION).equalsIgnoreCase("3")) {
                    realImage = functionsForPicture.rotateBitmap(realImage, 180 % 360);
                } else if (exif.getAttribute(ExifInterface.TAG_ORIENTATION).equalsIgnoreCase("0")) {
                    realImage = functionsForPicture.rotateBitmap(realImage, 270 % 360);
                }

                int heightLcl = getWindowManager().getDefaultDisplay().getHeight() - getActionBarHeight();
                int widthLcl = getWindowManager().getDefaultDisplay().getWidth();

                newBitmap = functionsForPicture.scaleCenterCrop(realImage, heightLcl, widthLcl);
                newBitmap.compress(Bitmap.CompressFormat.PNG, 85, fos);
                fos.close();

                imageSaved = true;

                FrontCameraActivity.this.runOnUiThread(new Runnable() {
                    public void run() {
                        if (FrontCameraActivity.this.mProgressDialog != null) {
                            FrontCameraActivity.this.mProgressDialog.cancel();
                            FrontCameraActivity.this.mProgressDialog = null;
                        }
                    }
                });

                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        try {
                            if (shotBtn != null) {
                                shotBtn.setText(imageSaved ? getResources().getString(R.string.camera_back)
                                        : getResources().getString(R.string.snapshot));
                            }
                        } catch (Exception e) {
                            e.printStackTrace();
                        }
                    }
                });
            } catch (FileNotFoundException e) {
                e.printStackTrace();
            } catch (IOException e) {
                e.printStackTrace();

            }
            camera.startPreview();
        }
    };

    private int getActionBarHeight() {
        int actionBarHeight = 0;
        try {
            TypedValue tv = new TypedValue();
            if (getTheme().resolveAttribute(android.R.attr.actionBarSize, tv, true))
                actionBarHeight = TypedValue.complexToDimensionPixelSize(tv.data, getResources().getDisplayMetrics());
        } catch (Exception e) {
            e.printStackTrace();
        }
        return actionBarHeight;
    }

    @Override
    public void onAutoFocus(boolean paramBoolean, Camera paramCamera) {
        /*if (paramBoolean) {
            paramCamera.takePicture(null, null, null, this);
        }*/
    }

    @Override
    public void onPreviewFrame(byte[] paramArrayOfByte, Camera paramCamera) {
        // тут можна обробляти зображення, яке відображається в preview
    }
}