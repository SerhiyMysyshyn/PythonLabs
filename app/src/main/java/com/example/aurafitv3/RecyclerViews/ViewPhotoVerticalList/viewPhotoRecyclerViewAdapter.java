package com.example.aurafitv3.RecyclerViews.ViewPhotoVerticalList;

import android.content.Context;
import android.graphics.drawable.Drawable;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.TextView;
import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.example.aurafitv3.R;
import java.io.File;
import java.util.HashMap;


public class viewPhotoRecyclerViewAdapter extends RecyclerView.Adapter<viewPhotoRecyclerViewAdapter.ViewHolder> {

    private HashMap<Integer, Drawable> itemData = new HashMap<>();
    private File[] jpgPathsArrayLcl;
    public Context context;

    public viewPhotoRecyclerViewAdapter(HashMap<Integer, Drawable> itemData, File[] jpgPathsArrayLcl, Context context) {
        this.itemData = itemData;
        this.jpgPathsArrayLcl = jpgPathsArrayLcl;
        this.context = context;
    }

    @NonNull
    @Override
    public viewPhotoRecyclerViewAdapter.ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View v = LayoutInflater.from(parent.getContext()).inflate(R.layout.recycler_view_item_2, parent, false);
        return new viewPhotoRecyclerViewAdapter.ViewHolder(v);
    }

    @Override
    public void onBindViewHolder(@NonNull viewPhotoRecyclerViewAdapter.ViewHolder holder, int position) {
        holder.mImage.setImageDrawable(itemData.get(position));
        holder.myTextView.setText(jpgPathsArrayLcl[position].getName());
    }

    @Override
    public int getItemCount() {
        return itemData.size();
    }


    public static class ViewHolder extends RecyclerView.ViewHolder{

        ImageView mImage;
        TextView myTextView;

        ViewHolder(View itemView) {
            super(itemView);
            mImage = itemView.findViewById(R.id.list_img);
            myTextView = itemView.findViewById(R.id.list_img_name);

        }

    }
}

