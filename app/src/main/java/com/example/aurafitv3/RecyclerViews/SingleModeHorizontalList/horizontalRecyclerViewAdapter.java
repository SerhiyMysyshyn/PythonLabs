package com.example.aurafitv3.RecyclerViews.SingleModeHorizontalList;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.example.aurafitv3.R;

import java.util.List;

public class horizontalRecyclerViewAdapter extends RecyclerView.Adapter<horizontalRecyclerViewAdapter.ViewHolder> {

    private List<Integer> mImagesColors;
    private List<String> mPercentage;
    public Context context;

    public horizontalRecyclerViewAdapter(List<Integer> mImagesColors, List<String> mPercentage, Context context) {
        this.mImagesColors = mImagesColors;
        this.mPercentage = mPercentage;
        this.context = context;
    }

    @NonNull
    @Override
    public horizontalRecyclerViewAdapter.ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View v = LayoutInflater.from(parent.getContext()).inflate(R.layout.recycler_view_item_1, parent, false);
        return new horizontalRecyclerViewAdapter.ViewHolder(v);
    }

    @Override
    public void onBindViewHolder(@NonNull horizontalRecyclerViewAdapter.ViewHolder holder, int position) {
        int color = mImagesColors.get(position);
        String percentage = mPercentage.get(position);

        holder.myTextView.setText(percentage);
        holder.mImage.setColorFilter(color);
    }

    @Override
    public int getItemCount() {
        return mImagesColors.size();
    }


    public static class ViewHolder extends RecyclerView.ViewHolder{

        ImageView mImage;
        TextView myTextView;

        ViewHolder(View itemView) {
            super(itemView);
            myTextView = itemView.findViewById(R.id.percentage_suitable_aura);
            mImage = itemView.findViewById(R.id.different_aura_images);
        }

    }
}
