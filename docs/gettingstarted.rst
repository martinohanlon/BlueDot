Getting Started
===============

In order to use Blue Dot you will need:

* A Raspberry Pi

  - with built-in Bluetooth (such as the Pi 3 or Pi Zero W)
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

    sudo apt install python3-dbus
    sudo pip3 install bluedot

If you want to use Blue Dot with Python 2 (there really is no need though!)::

    sudo apt install python-dbus
    sudo pip install bluedot

To upgrade to the latest version::

    sudo pip3 install bluedot --upgrade

Pairing
-------

In order to use Blue Dot you will need to pair the Raspberry Pi to the remote
:doc:`Android phone <pairpiandroid>` or :doc:`2nd Raspberry Pi <pairpipi>`.

Code
----

1. Start up Python 3 (select :menuselection:`Menu --> Programming --> Python
   3`)

2. Select :menuselection:`File --> New File` to create a new program

3. Enter the following code::

       from bluedot import BlueDot
       bd = BlueDot()
       bd.wait_for_press()
       print("You pressed the blue dot!")

4. Save your program (select :menuselection:`File --> Save As`) and save as
   :file:`mydot.py`

5. Run the program, (select :menuselection:`Run --> Run Module` or press
   :kbd:`F5`)

.. warning::

    Do not save your program as :file:`bluedot.py` as Python will try and
    import your program rather than the bluedot module and you will get the
    error ``ImportError: cannot import name BlueDot``.

Connecting
----------

Start-up the `Blue Dot app`_ on your Android phone or run the
:doc:`bluedotpythonapp` on your 2nd Raspberry Pi:

1. Select your Raspberry Pi from the list

2. Press the Blue Dot

Where next
----------

Check out the :doc:`recipes` and the :doc:`dotapi` documentation for more ideas
on using Blue Dot.

.. _Blue Dot app: http://play.google.com/store/apps/details?id=com.stuffaboutcode.bluedot
.. _Raspbian: https://www.raspberrypi.org/downloads/raspbian/
