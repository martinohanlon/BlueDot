package com.stuffaboutcode.bluedot;

import androidx.appcompat.app.AppCompatActivity;

import android.content.pm.PackageManager;
import android.os.Bundle;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.widget.ImageButton;
import android.widget.Toast;
import android.content.Intent;
import android.widget.ArrayAdapter;
import android.widget.AdapterView;
import android.widget.ListView;
import android.widget.TextView;
import android.view.View;
import android.net.Uri;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;

import androidx.core.app.ActivityCompat;
import androidx.preference.PreferenceManager;
import android.content.SharedPreferences;
import android.Manifest;

import java.util.Set;
import java.util.ArrayList;

public class Devices
        extends AppCompatActivity
        implements SharedPreferences.OnSharedPreferenceChangeListener {

    ListView devicelist;
    ImageButton infoButton;

    private BluetoothAdapter myBluetooth = null;
    private Set<BluetoothDevice> pairedDevices;
    public static String EXTRA_ADDRESS = "device_address";
    public static String EXTRA_NAME = "device_name";

    private static String[] PERMISSIONS = {
            Manifest.permission.BLUETOOTH_SCAN,
            Manifest.permission.BLUETOOTH_CONNECT,

    };

    private void checkPermissions(){
        int permission = ActivityCompat.checkSelfPermission(this, Manifest.permission.BLUETOOTH_CONNECT);
        if (permission != PackageManager.PERMISSION_GRANTED) {
            // We don't have permission so prompt the user
            ActivityCompat.requestPermissions(
                    this,
                    PERMISSIONS,
                    1
            );
        }
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_devices);

        devicelist = (ListView)findViewById(R.id.listView);

        checkPermissions();

        //if the device has bluetooth
        myBluetooth = BluetoothAdapter.getDefaultAdapter();

        if(myBluetooth == null) {
            Toast.makeText(
                    getApplicationContext(),
                    "Bluetooth Device Not Available",
                    Toast.LENGTH_LONG).show();

            //finish apk
            this.finish();
            System.exit(0);

        } else if(!myBluetooth.isEnabled()) {
            //Ask to the user turn the bluetooth on
            Intent turnBTon = new Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE);
            startActivityForResult(turnBTon,1);
        }

        SharedPreferences sharedPreferences = PreferenceManager.getDefaultSharedPreferences(this);
        sharedPreferences.registerOnSharedPreferenceChangeListener(this);
    }

    @Override
    protected void onResume() {
        super.onResume();
        setConnectMsg();
        pairedDevicesList();
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        MenuInflater menuInflater = getMenuInflater();
        menuInflater.inflate(R.menu.settings_menu, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        int id = item.getItemId();
        if (id == R.id.settings) {
            Intent intent = new Intent(Devices.this, SettingsActivity.class);
            startActivity(intent);
            return true;
        } else if (id == R.id.help) {
            Uri uri = Uri.parse("https://bluedot.readthedocs.io");
            Intent intent = new Intent(Intent.ACTION_VIEW, uri);
            startActivity(intent);
            return true;
        }
        return super.onOptionsItemSelected(item);
    }

    @Override
    public void onSharedPreferenceChanged(SharedPreferences sharedPreferences, String key) {

        if (key.equals("port")) {
            setConnectMsg(sharedPreferences);
        }
    }

    private void setConnectMsg() {
        SharedPreferences sharedPreferences = PreferenceManager.getDefaultSharedPreferences(this);
        setConnectMsg(sharedPreferences);
    }

    private void setConnectMsg(SharedPreferences sharedPreferences) {
        String message = "Connect";
        Boolean default_port = sharedPreferences.getBoolean("default_port", true);
        String port_value = sharedPreferences.getString("port", "1");

        if (!default_port) {
            message = message + " on port " + port_value;
        }

        TextView connectView = findViewById(R.id.connect);
        connectView.setText(message);
    }

    private void pairedDevicesList() {
        pairedDevices = myBluetooth.getBondedDevices();
        ArrayList<String> list = new ArrayList<String>();

        if (pairedDevices.size()>0) {
            // create a list of paired bluetooth devices
            for(BluetoothDevice bt : pairedDevices)
            {
                list.add(bt.getName() + "\n" + bt.getAddress()); //Get the device's name and the address
            }
        } else {
            Toast.makeText(
                    getApplicationContext(),
                    "No Paired Bluetooth Devices Found.",
                    Toast.LENGTH_LONG).show();
        }

        final ArrayAdapter adapter = new ArrayAdapter(this,android.R.layout.simple_list_item_1, list);
        devicelist.setAdapter(adapter);
        devicelist.setOnItemClickListener(myListClickListener); //Method called when the device from the list is clicked
    }

    private AdapterView.OnItemClickListener myListClickListener = new AdapterView.OnItemClickListener()
    {
        public void onItemClick (AdapterView<?> av, View v, int arg2, long arg3)
        {
            // Get the device MAC address, the last 17 chars in the View
            String info = ((TextView) v).getText().toString();
            String deviceName = info.split("\n")[0];
            String address = info.split("\n")[1];

            // Make an intent to start next activity.
            Intent i = new Intent(Devices.this, Button.class);

            //Change the activity.
            i.putExtra(EXTRA_NAME, deviceName);
            i.putExtra(EXTRA_ADDRESS, address);
            startActivity(i);
        }
    };


}

