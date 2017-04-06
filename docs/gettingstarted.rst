Getting started
===============

installation
------------

These instructions assume your Raspberry Pi is running the latest version of `Raspbian`_ with Pixel. 

app
~~~

After alpha the `Blue Dot app`_ will be available from the Google Play Store - until then you can download `here 
<https://github.com/martinohanlon/BlueDot/blob/master/clients/android/app/app-release.apk?raw=true>`_. You will have to enable `installation from unknown sources`_ in order to do so.

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

1. Enter the same PIN code when prompter
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

4. Run the program, click ``Run > Run Module`` or press ``F5``

connect
~~~~~~~

Start the `Blue Dot app`_, connect to your Raspberry Pi, press the blue dot. 

.. _Blue Dot app: https://github.com/martinohanlon/BlueDot/blob/master/clients/android/app/app-release.apk?raw=true
.. _installation from unknown sources: https://www.applivery.com/docs/troubleshooting/android-unknown-sources
.. _Raspbian: https://www.raspberrypi.org/downloads/raspbian/