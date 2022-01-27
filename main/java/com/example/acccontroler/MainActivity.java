package com.example.acccontroler;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Context;
import android.content.DialogInterface;
import android.content.pm.ActivityInfo;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.net.wifi.WifiManager;
import android.os.Bundle;
import android.text.Editable;
import android.text.Html;
import android.text.TextWatcher;
import android.text.format.Formatter;
import android.view.Gravity;
import android.view.KeyEvent;
import android.view.View;
import android.view.inputmethod.EditorInfo;
import android.view.inputmethod.InputMethodManager;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import java.io.IOException;
import java.io.OutputStream;
import java.io.PrintWriter;
import java.net.InetAddress;
import java.net.Socket;
import java.util.Locale;

public class MainActivity extends AppCompatActivity
{
    // Display
    DisplayView displayView;

    // Server info
    private String SERVER_IP = "192.168.1.58";
    private final int SERVER_PORT = 8000;
    private Socket clientSocket;
    private PrintWriter output;
    private String outString = String.valueOf(.0) + "," + String.valueOf(.0) + "," + String.valueOf(.0);
    private EditText ipText;

    // Accelerometer variables
    private final float threshold = 0.f;
    private int pause = 10; // ms
    private long last = System.currentTimeMillis();

    private TextView currentIP;
    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);


        // Lock screen
        this.setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_LOCKED);

        //Get display view
        displayView = findViewById(R.id.canvas);


        // Set up the sensors
        SensorManager sensorManager = (SensorManager) getSystemService(SENSOR_SERVICE);
        Sensor accSensor = sensorManager.getDefaultSensor(Sensor.TYPE_GRAVITY);

        // Create a listener
        SensorEventListener accSensorListener = new SensorEventListener()
        {
            @Override
            public void onSensorChanged(SensorEvent sensorEvent)
            {
                float x = sensorEvent.values[0];
                float y = sensorEvent.values[1];
                float z = sensorEvent.values[2];

                long elapsed = System.currentTimeMillis() - last;
                last = System.currentTimeMillis();

                if (elapsed < pause)
                    return;

                // Draw the arrow
                displayView.update(x, y);

                outString = String.valueOf(x) + "," + String.valueOf(y) + "," + String.valueOf(z);
                new Thread(socketThread).start();

            }

            @Override
            public void onAccuracyChanged(Sensor sensor, int i) { }
        };

        // Register the listener
        sensorManager.registerListener(
                accSensorListener,
                accSensor,
                SensorManager.SENSOR_DELAY_GAME);

        ipText = (EditText) findViewById(R.id.ip_address);
        currentIP = (TextView)  findViewById(R.id.current_ip);
        currentIP.setText("Current IP: " + SERVER_IP);


        //ipText.setOnEditorActionListener(new DoneOnEditorActionListener());
        ipText.setHint("IP address: " + SERVER_IP);
        ipText.setOnKeyListener((view, keyCode, keyEvent) ->
        {
            if ((keyEvent.getAction() == KeyEvent.ACTION_DOWN))// && (keyCode == KeyEvent.KEYCODE_BREAK))
            {
                // Set IP
                SERVER_IP = ipText.getText().toString();
                ipText.setHint("IP address: " + SERVER_IP);
                currentIP.setText("Current IP: " + SERVER_IP);

                // Print toast
                Context context = getApplicationContext();
                CharSequence text = "IP CHANGED!";
                Toast toast = Toast.makeText(context, text, Toast.LENGTH_SHORT);
                toast.setGravity(Gravity.CENTER, 0, 0);
                toast.show();
                ipText.clearFocus();
                displayView.requestFocus();
                return true;
            }
            return false;
        });
    }

    private final Runnable socketThread = new Runnable()
    {
        @Override
        public void run()
        {
            try
            {
                InetAddress serverAddr = InetAddress.getByName(SERVER_IP);
                clientSocket = new Socket(serverAddr, SERVER_PORT);
                OutputStream out = clientSocket.getOutputStream();
                output = new PrintWriter(out);
                output.print(outString);

                output.flush();

                output.close();
                out.close();
                clientSocket.close();
            }
            catch (IOException e)
            {
                e.printStackTrace();
            }
        }
    };
}