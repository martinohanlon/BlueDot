Getting started
===============

installation
------------

These instructions assume your Raspberry Pi is running the latest version of `Raspbian`_ with Pixel. 

You will need a Raspberry Pi with built-in Bluetooth (such as the Pi 3 or Pi Zero W) or Raspberry Pi and a USB bluetooth dongle.

app
~~~

The `Blue Dot app`_ is available from the Google Play Store `here 
<http://play.google.com/store/apps/details?id=com.stuffaboutcode.bluedot>`_.

python library
~~~~~~~~~~~~~~

Open a terminal, click ``Menu > Accessories > Terminal``::

    sudo apt-get install python3-dbus
    sudo pip3 install bluedot

If you want to use bluedot with Python 2 (there really is no need though!)::

    sudo apt-get install python-dbus
    sudo pip install bluedot

usage
-----

pair
~~~~

In order to connect the Blue Dot app you will need to pair the client (android phone) to the Raspberry Pi.

On your Android phone

1. Open Settings
2. Select Bluetooth 
3. This will make your phone Discoverable

Using your Raspberry Pi

1. Click the bluetooth icon on the taskbar
2. Turn on Bluetooth (if its off)
3. Click `Make Discoverable`
4. Click Add Device
5. Your phone will appear in the list, select it and click Pair
6. Enter a PIN code

On your Android phone

1. Enter the same PIN code when prompted
2. Click Ok

Your Raspberry Pi and Android phone are now paired.

write code
~~~~~~~~~~

1. Start up Python 3, click ``Menu > Programming > Python 3``
2. Click ``File > New File`` to create a new program
3. Create your python program::

    from bluedot import BlueDot
    bd = BlueDot()
    bd.wait_for_press()
    print("You pressed the blue dot!")

4. Save your program, click ``File > Save As`` and save as ``mydot.py``
5. Run the program, click ``Run > Run Module`` or press ``F5``

Warning - do not save your program as ``bluedot.py`` as Python will try and import your program rather than the bluedot module and you will get the error ``ImportError: cannot import name BlueDot``.

connect
~~~~~~~

Start the `Blue Dot app`_, select your Raspberry Pi from the list to connect, press the blue dot. 

.. _Blue Dot app: http://play.google.com/store/apps/details?id=com.stuffaboutcode.bluedot
.. _Raspbian: https://www.raspberrypi.org/downloads/raspbian/