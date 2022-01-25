package com.example.aurafitv3;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.view.View;
import android.widget.LinearLayout;
import android.widget.Toast;

public class PartnersMode extends AppCompatActivity {

    LinearLayout mCompatibilitybtn;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_partners_mode);

        mCompatibilitybtn = (LinearLayout)findViewById(R.id.partnersMode_check_compatibility_button);
        mCompatibilitybtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Toast.makeText(getApplicationContext(), "Pressed Compatibility button", Toast.LENGTH_LONG).show();
            }
        });

    }
}