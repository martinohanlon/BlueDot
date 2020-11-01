Getting Started
===============

In order to use Blue Dot you will need:

* A Raspberry Pi

  - with built-in Bluetooth (such as the Raspberry Pi 3, 4 or Zero W)
  - or a USB Bluetooth dongle

* An Android phone or 2nd Raspberry Pi for the remote
* An Internet connection (for the install)

Installation
------------

These instructions assume your Raspberry Pi is running the latest version of
`Raspbian`_.

Android App
~~~~~~~~~~~

If you're using an Android phone, the `Blue Dot app`_ can be installed from the
Google Play Store.

Python Library
~~~~~~~~~~~~~~

Open a terminal (click :menuselection:`Menu --> Accessories --> Terminal`),
then enter::

    sudo pip3 install bluedot

To upgrade to the latest version::

    sudo pip3 install bluedot --upgrade

Pairing
-------

In order to use Blue Dot you will need to pair the Raspberry Pi to the remote
:doc:`Android phone <pairpiandroid>` or :doc:`2nd Raspberry Pi <pairpipi>`.

Code
----

1. Start up Python 3 (e.g. :menuselection:`Menu --> Programming --> Thonny Python
   IDE`)

2. Create a new program

3. Enter the following code::

    from bluedot import BlueDot
    bd = BlueDot()
    bd.wait_for_press()
    print("You pressed the blue dot!")

4. Save your program as :file:`mydot.py`

5. Run the program::

    Server started ##:##:##:##:##:##
    Waiting for connection

.. warning::

    Do not save your program as :file:`bluedot.py` as Python will try and
    import your program rather than the bluedot module and you will get the
    error ``ImportError: cannot import name BlueDot``.

Connecting
----------

Start-up the `Blue Dot app`_ on your Android phone or run the
:doc:`bluedotpythonapp` on your 2nd Raspberry Pi:

1. Select your Raspberry Pi from the list

.. note::

    Your python program will need to be running and ``Waiting for connection`` 
    before the BlueDot app will be able to connect to your Raspberry Pi.

2. Press the Blue Dot

Where next
----------

Check out the :doc:`recipes` and the :doc:`dotapi` documentation for more ideas
on using Blue Dot.

.. _Blue Dot app: http://play.google.com/store/apps/details?id=com.stuffaboutcode.bluedot
.. _Raspbian: https://www.raspberrypi.org/downloads/raspbian/
