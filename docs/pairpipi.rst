Pair 2 raspberry pi's
=========================

The instructions below describe Raspberry Pi 1 and 2, it doesn't matter which Pi is 1 and which is 2.

Using the Desktop
-------------------------

On Raspberry Pi 1:

1. Click the bluetooth icon on the taskbar
2. Turn on Bluetooth (if its off)
3. Click `Make Discoverable`

On Raspberry Pi 2:

1. Click the bluetooth icon on the taskbar
2. Turn on Bluetooth (if its off)
3. Click `Make Discoverable`
4. Click Add Device
5. Pi 1 will appear in the list, select it and click Pair

On Raspberry Pi 1:

1. Accept the pairing request

You may receive errors relating to services not being able available or being unable to connect, these can be ignored.

Using the Command Line
-------------------------

On Raspberry Pi 1:

1. Type ``bluetoothctl`` and press Enter to open Bluetooth control 
2. At the ``[bluetooth]$`` prompt enter the following commands::

    discoverable on
    pairable on
    agent on
    default-agent

On Raspberry Pi 2:

1. Type ``bluetoothctl`` and press Enter to open Bluetooth control 
2. At the ``[bluetooth]$`` prompt enter the following commands::

    discoverable on
    pairable on
    agent on
    default-agent
    scan on

3. Wait for a message to appear showing Pi 1 has been found::

    [NEW] Device 12:23:34:45:56:67 devicename

4. Type pair with the mac address of Pi 1::

    pair 12:23:34:45:56:67

5. Enter a PIN

On Raspberry Pi 1:

1. Enter the same PIN when prompted
2. Type ``exit`` and press Enter to return to the command line 

