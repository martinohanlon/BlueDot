Getting started
===============

Installation
------------

Blue Dot App
~~~~~~~~~~~~~~~

After alpha the Blue Dot app will be available from the Google Play Store - until then you can download `here 
<https://github.com/martinohanlon/BlueDot/blob/android-dev/clients/android/app/app-release.apk?raw=true>`_.

The Blue Dot app is available from the Android Play Store - tbc.

Python library
~~~~~~~~~~~~~~

Open a terminal, click ``Menu > Accessories > Terminal``::

    sudo apt-get install python3-dbus
    sudo pip3 install bluedot

Usage
-----

Pairing
~~~~~~~

In order to connect the Blue Dot app you will need to pair the client (android phone) to the Raspberry Pi.

Using your Raspberry Pi

1. Click the bluetooth icon on the taskbar
2. Turn on Bluetooth (if its off)
3. Click `Make Discoverable`

On your Android phone

1. Open Settings
2. Select Bluetooth
3. Your Raspberry Pi will appear in the `Available devices` list
4. Select your Raspberry Pi, and click Pair

Raspberry Pi

1. Agree to the pairing request
2. (You may receive and error  relating to no services being available - this can be ignored)

Your Raspberry Pi and Android phone are now paired.

Python program
~~~~~~~~~~~~~~

1. Start up Python 3, click ``Menu > Programming > Python 3``
2. Click ``File > New File`` to create a new program
3. Create your python program::

    from bluedot import BlueDot
    dot = BlueDot()
    dot.wait_for_press()
    print("You pressed the blue dot!")

4. Run the program, click ``Run > Run Module`` or press ``F5``

Blue Dot App
~~~~~~~~~~~~

Start the BlueDot app, connect to your Raspberry Pi, press the blue dot. 


.. _AppDownload: https://github.com/martinohanlon/BlueDot/blob/android-dev/clients/android/app/app-release.apk?raw=true
