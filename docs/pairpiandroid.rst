Pair a Raspberry Pi and Android phone
=====================================

Using the Desktop
-----------------

On your Android phone:

1. Open Settings

2. Select Bluetooth and make your phone "discoverable"

On your Raspberry Pi:

1. Click :menuselection:`Bluetooth --> Turn On Bluetooth` (if it's off)

2. Click :menuselection:`Bluetooth --> Make Discoverable`

3. Click :menuselection:`Bluetooth --> Add Device`

4. Your phone will appear in the list, select it and click :guilabel:`Pair`

On your Android phone and Raspberry Pi.

1. Confirm the pairing code matches

2. Click OK

.. note::

    You may receive errors relating to services not being able available or being unable to connect: these can be ignored, your phone and Raspberry Pi are now paired.

Using the Command Line
----------------------

On your Android phone:

1. Open Settings

2. Select Bluetooth and make your phone "discoverable"

On your Raspberry Pi:

1. Type :command:`bluetoothctl` and press Enter to open Bluetooth control

2. At the ``[bluetooth]#`` prompt enter the following commands::

       discoverable on
       pairable on
       agent on
       default-agent
       scan on

3. Wait for a message to appear showing the Android phone has been found::

       [NEW] Device 12:23:34:45:56:67 devicename

4. Type pair with the mac address of your Android phone::

       pair 12:23:34:45:56:67

On your Android phone and Raspberry Pi.

1. Confirm the passcode.

2. Type :command:`quit` and press Enter to return to the command line