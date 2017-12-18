Pair a Raspberry Pi and Android phone
=====================================

Using the Desktop
-----------------

On your Android phone:

1. Open Settings

2. Select Bluetooth

3. This will make your phone "discoverable"

On your Raspberry Pi:

1. Click :menuselection:`Bluetooth --> Turn On Bluetooth` (if it's off)

2. Click :menuselection:`Bluetooth --> Make Discoverable`

3. Click :menuselection:`Bluetooth --> Add Device`

4. Your phone will appear in the list, select it and click guilabel:`Pair`

5. Enter a PIN code

On your Android phone again:

1. Enter the same PIN code when prompted

2. Touch "OK"

.. note::

    You may receive errors relating to services not being able available or being unable to connect: these can be ignored.

Using the Command Line
----------------------

On your Raspberry Pi:

1. Type :command:`bluetoothctl` and press Enter to open Bluetooth control

2. At the ``[bluetooth]#`` prompt enter the following commands::

       discoverable on
       pairable on
       agent on
       default-agent

On your Android phone:

1. Open Settings

2. Select Bluetooth

3. Your Raspberry Pi will appear in the list; select it

4. Enter a PIN

On your Raspberry Pi:

1. Re-enter the PIN

2. Type :command:`quit` and press Enter to return to the command line
