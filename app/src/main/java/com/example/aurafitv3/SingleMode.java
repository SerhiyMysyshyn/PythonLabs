package com.example.aurafitv3;

import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.graphics.Color;
import android.os.Bundle;
import android.view.View;
import android.widget.LinearLayout;
import android.widget.Toast;

import com.example.aurafitv3.RecyclerViews.SingleModeHorizontalList.horizontalRecyclerViewAdapter;
import com.example.aurafitv3.RecyclerViews.SingleModeHorizontalList.horizontalRecyclerViewClickListener;

import java.util.ArrayList;

public class SingleMode extends AppCompatActivity{

    private horizontalRecyclerViewAdapter adapter;

    LinearLayout mCompatibilitybtn;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_single_mode);

        mCompatibilitybtn = (LinearLayout)findViewById(R.id.singleMode_check_compatibility_button);
        mCompatibilitybtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Toast.makeText(getApplicationContext(), "Pressed Compatibility button", Toast.LENGTH_LONG).show();
            }
        });


        ArrayList<Integer> imageColors = new ArrayList<>();
        imageColors.add(Color.BLUE);
        imageColors.add(Color.YELLOW);
        imageColors.add(Color.MAGENTA);
        imageColors.add(Color.RED);
        imageColors.add(Color.BLACK);

        ArrayList<String> imagePercentages = new ArrayList<>();
        imagePercentages.add("100%");
        imagePercentages.add("75%");
        imagePercentages.add("60%");
        imagePercentages.add("30%");
        imagePercentages.add("20%");

        RecyclerView recyclerView = findViewById(R.id.aura_types_rv);
        LinearLayoutManager horizontalLayoutManager
                = new LinearLayoutManager(SingleMode.this, LinearLayoutManager.HORIZONTAL, false);
        recyclerView.setLayoutManager(horizontalLayoutManager);
        adapter = new horizontalRecyclerViewAdapter(imageColors, imagePercentages, this);
        recyclerView.setAdapter(adapter);


        recyclerView.addOnItemTouchListener(new horizontalRecyclerViewClickListener(this, new horizontalRecyclerViewClickListener.OnItemClickListener() {
            @Override
            public void onItemClick(View view, int position) {
                Toast.makeText(getApplicationContext(), "Pressed "+position, Toast.LENGTH_LONG).show();
            }
        }));



    }
}