package com.example.aurafitv3.camera;

import android.app.Activity;
import android.content.Context;
import android.content.SharedPreferences;
import android.graphics.Bitmap;
import android.graphics.Canvas;
import android.graphics.Matrix;
import android.graphics.RectF;
import android.os.Environment;
import android.util.TypedValue;

import java.io.File;
import java.util.Date;

public class FunctionsForPicture extends Activity{

    private SharedPreferences preferencesData;
    private String path;
    private int width;
    private int height;

    public static final int JPG_TYPE_IMAGE = 1;

// -------------------------------------------------------------------------------------------------------------------------------------------------
    public File getOutputMediaFile(int mediaTypeImage, Context context) {
        preferencesData = context.getSharedPreferences("aurafit", Context.MODE_PRIVATE);

        File mediaStorageDir = new File(Environment.getExternalStoragePublicDirectory(
                Environment.DIRECTORY_PICTURES), "Aura iTrain V3");

        if (!mediaStorageDir.exists()) {
            if (!mediaStorageDir.mkdirs()) {
                return null;
            }
        }

        String userName = preferencesData.getString("user_name_1","");
        String timeStamp = "" + new Date().getTime();
        File mediaFile;
        String lcl;
        if (mediaTypeImage == JPG_TYPE_IMAGE)
            lcl = ".jpg";
        else
            lcl = ".png";
        String prefix = "";
        if (userName != null && userName.length() > 0) {
            prefix = userName + "_";
        } else {
            prefix = "IMG_";
        }
        path = mediaStorageDir.getPath() + File.separator +
                prefix + timeStamp + lcl;
        mediaFile = new File(path);

        SharedPreferences.Editor editorLcl = preferencesData.edit();
        editorLcl.putString("path", path);
        editorLcl.apply();

        //System.out.println(">>> Path: " + path);

        return mediaFile;
    }

// -------------------------------------------------------------------------------------------------------------------------------------------------
    public Bitmap scaleCenterCrop(Bitmap source, int newHeight, int newWidth) {
        int sourceWidth = source.getWidth();
        int sourceHeight = source.getHeight();

        if (newHeight == 0 || newWidth == 0) {
            newHeight = height;
            newWidth = width;
        }

        float xScale = (float) newWidth / sourceWidth;
        float yScale = (float) newHeight / sourceHeight;
        float scale = Math.max(xScale, yScale);
        float scaledWidth = scale * sourceWidth;
        float scaledHeight = scale * sourceHeight;
        float left = (newWidth - scaledWidth) / 2;
        float top = (newHeight - scaledHeight) / 2;

        RectF targetRect = new RectF(left, top, left + scaledWidth, top + scaledHeight);

        Bitmap dest = Bitmap.createBitmap(newWidth, newHeight, source.getConfig());
        Canvas canvas = new Canvas(dest);
        canvas.drawBitmap(source, null, targetRect, null);

        return dest;
    }

// Поворот зображення ---------------------------------------------------------------------------------------------------------------------------
    public Bitmap rotateBitmap(Bitmap source, int angle) {
        Matrix matrix = new Matrix();
        matrix.postRotate(angle);
        if (angle % 180 != 0)
            return Bitmap.createBitmap(source, 0, 0, source.getWidth(), source.getHeight(), matrix, true);
        else
            return Bitmap.createBitmap(source, 0, 0, source.getHeight(), source.getWidth(), matrix, true);
    }

// Визначаю висоту ActionBar ---------------------------------------------------------------------------------------------------------------------
    /*private int getActionBarHeight() {
        int actionBarHeight = 0;
        try {
            TypedValue tv = new TypedValue();
            if (getTheme().resolveAttribute(android.R.attr.actionBarSize, tv, true))
                actionBarHeight = TypedValue.complexToDimensionPixelSize(tv.data, getResources().getDisplayMetrics());
        } catch (Exception e) {
            e.printStackTrace();
        }
        return actionBarHeight;
    }*/


}
