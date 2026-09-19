package com.sanabi.kakaotheme;

import android.app.Activity;
import android.os.Bundle;
import android.graphics.Color;
import android.view.Gravity;
import android.widget.TextView;

public class MainActivity extends Activity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        TextView textView = new TextView(this);

        textView.setText("SANABI 블랙 테마");
        textView.setTextColor(Color.WHITE);
        textView.setBackgroundColor(Color.BLACK);
        textView.setTextSize(24);
        textView.setGravity(Gravity.CENTER);

        setContentView(textView);
    }
}
