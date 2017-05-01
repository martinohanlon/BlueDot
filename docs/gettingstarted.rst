Getting started
===============

what
----

In order to use Blue Dot you will need:

* a Raspberry Pi

  * with built-in Bluetooth (such as the Pi 3 or Pi Zero W)
  * or a USB Bluetooth dongle

* an Android phone or 2nd Raspberry Pi for the remote
* an internet connection (for the install)

installation
------------

These instructions assume your Raspberry Pi is running the latest version of `Raspbian`_ with Pixel. 

android app
~~~~~~~~~~~

If using an Android phone, the `Blue Dot app`_ can be installed from the Google Play Store.

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

In order to use Blue Dot you will need to pair the Raspberry Pi to the remote (`Android phone`_ or `2nd Raspberry Pi`_).

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

Start-up the `Blue Dot app`_ on your Android phone or run the `Blue Dot python app`_ on your 2nd Raspberry Pi:
 1. Select your Raspberry Pi from the list
 2. Press the blue dot
 
where next
----------

Check out the `Recipes`_ and the `API`_ documentation for more ideas on using bluedot.  

.. _Blue Dot app: http://play.google.com/store/apps/details?id=com.stuffaboutcode.bluedot
.. _Raspbian: https://www.raspberrypi.org/downloads/raspbian/
.. _Recipes: recipes.html
.. _API: dotapi.html
.. _2nd Raspberry Pi: pairpipi.html
.. _Android phone: pairpiandroid.html
.. _Blue Dot python app: bluedotpythonapp.html