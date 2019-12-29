package com.stuffaboutcode.bluedot;

import android.os.Bundle;

import androidx.appcompat.app.ActionBar;
import androidx.appcompat.app.AppCompatActivity;
import androidx.preference.PreferenceFragmentCompat;
import androidx.preference.Preference;
import androidx.preference.ListPreference;
import androidx.preference.SwitchPreferenceCompat;
import android.content.SharedPreferences;

public class SettingsActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.settings_activity);

        getSupportFragmentManager()
                .beginTransaction()
                .replace(R.id.settings, new SettingsFragment())
                .commit();

        ActionBar actionBar = getSupportActionBar();

        if (actionBar != null) {
            actionBar.setDisplayHomeAsUpEnabled(true);
        }

    }

    public static class SettingsFragment
            extends PreferenceFragmentCompat
            implements SharedPreferences.OnSharedPreferenceChangeListener{

        @Override
        public void onCreatePreferences(Bundle savedInstanceState, String rootKey) {
            setPreferencesFromResource(R.xml.root_preferences, rootKey);

            setupPreferences();
        }

        @Override
        public void onResume() {
            super.onResume();

            getPreferenceScreen().getSharedPreferences()
                    .registerOnSharedPreferenceChangeListener(this);
        }

        @Override
        public void onPause() {
            super.onPause();

            getPreferenceScreen().getSharedPreferences()
                    .unregisterOnSharedPreferenceChangeListener(this);
        }

        @Override
        public void onSharedPreferenceChanged(SharedPreferences sharedPreferences,String key) {
            setupPreferences();
        }

        private void setupPreferences() {
            Preference auto_port = findPreference("auto_port");
            SwitchPreferenceCompat auto_port_switch = (SwitchPreferenceCompat)auto_port;
            Preference port = findPreference("port");
            ListPreference port_list = (ListPreference) port;
            if (auto_port_switch != null) {
                if (port_list != null) {
                    // disable the port if the auto_port is enabled
                    if (auto_port_switch.isChecked()) port.setVisible(false);
                    else port.setVisible(true);
                    // set the port summary
                    port.setSummary(port_list.getEntry());
                }
            }
        }

    }
}