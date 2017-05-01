Pair raspberry pi and android phone
===================================

Using the Desktop
-------------------------

On your Android phone:

1. Open Settings
2. Select Bluetooth 
3. This will make your phone Discoverable

Using your Raspberry Pi:

1. Click the bluetooth icon on the taskbar
2. Turn on Bluetooth (if its off)
3. Click `Make Discoverable`
4. Click Add Device
5. Your phone will appear in the list, select it and click Pair
6. Enter a PIN code

On your Android phone:

1. Enter the same PIN code when prompted
2. Click Ok

Using the Command Line
-------------------------

Using your Raspberry Pi:

1. Type ``bluetoothctl`` and press Enter to open Bluetooth control 
2. At the ``[bluetooth]$`` prompt enter the following commands::

    discoverable on
    pairable on
    agent on
    default-agent

Using your Android phone:

1. Open Settings
2. Select Bluetooth 
3. Your Raspberry Pi will appear in the list, select it
4. Enter a PIN

Using your Raspberry Pi:

1. Re-enter the PIN
2. Type ``exit`` and press Enter to return to the command line 