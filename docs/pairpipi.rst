Pair 2 Raspberry Pis
====================

The instructions below describe pairing a couple of Raspberry Pis which either
have built-in Bluetooth (the Pi 3B or the Pi Zero W) or a USB Bluetooth dongle.

Using the Desktop
-----------------

On the first Raspberry Pi:

1. Click :menuselection:`Bluetooth --> Turn On Bluetooth` (if it's off)

2. Click :menuselection:`Bluetooth --> Make Discoverable`

On the second Raspberry Pi:

1. Click :menuselection:`Bluetooth --> Turn On Bluetooth` (if it's off)

2. Click :menuselection:`Bluetooth --> Make Discoverable`

3. Click :menuselection:`Bluetooth --> Add Device`

4. The first Pi will appear in the list: select it and click the :guilabel:`Pair` button

On the first Raspberry Pi again:

1. Accept the pairing request

.. note::

    You may receive errors relating to services not being able available or being unable to connect: these can be ignored.

Using the Command Line
----------------------

On the first Raspberry Pi:

1. Enter :command:`bluetoothctl` to open Bluetooth control

2. At the ``[bluetooth]#`` prompt enter the following commands::

       discoverable on
       pairable on
       agent on
       default-agent

On the second Raspberry Pi:

1. Enter :command:`bluetoothctl` to open Bluetooth control

2. At the ``[bluetooth]#`` prompt enter the following commands::

       discoverable on
       pairable on
       agent on
       default-agent
       scan on

3. Wait for a message to appear showing the first Pi has been found::

       [NEW] Device 12:23:34:45:56:67 devicename

4. Type pair with the mac address of the first Pi::

       pair 12:23:34:45:56:67

5. Enter a PIN

On the first Raspberry Pi again:

1. Enter the same PIN when prompted

2. Type :command:`quit` and press Enter to return to the command line
