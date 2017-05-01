Blue Dot Python Client
======================

Blue Dot Python client allows you to use another Raspberry Pi (or linux based computer) as the Blue Dot app.

|bluedotpython| |bluedotpythondevices|

start
-----

The client is included in the bluedot Python library:

1. Install the Python library as described in the `getting started`_ guide
2. Run the Blue Dot client::

    python3 -m bluedot.client

options
-------

To get help with the Blue Dot client options::

    python3 -m bluedot.client --help


    usage: client.py [-h] [--device DEVICE] [--server SERVER] [--fullscreen]
                     [--width WIDTH] [--height HEIGHT]

    Blue Dot Python Client

    optional arguments:
      -h, --help       show this help message and exit
      --device DEVICE  The name of the bluetooth device to use (default is hci0)
      --server SERVER  The name or mac address of the bluedot server
      --fullscreen     Fullscreen app
      --width WIDTH    A custom screen width (default is 320)
      --height HEIGHT  A customer screen height (default is 240)

You can specify the server to connect to at startup by using the ``--server`` option::

    python3 -m bluedot.client --server myraspberrypi

The screen size of the Blue Dot client can be changed using the ``width`` and ``height`` options and specifying the number of pixels:

    python3 -m bluedot.client --width 500 -- height 500

The client can also be used full screen, if no ``width`` or ``height`` is given the screen will be sized to the current resolution of the screen::

    python3 -m bluedot.client --fullscreen

If you have more than 1 bluetooth device you can use ``--device`` to use a particular device::

    python3 -m bluedot.client --device hci1

.. _getting started: http://bluedot.readthedocs.io/en/latest/gettingstarted.html

.. |bluedotpython| image:: https://raw.githubusercontent.com/martinohanlon/BlueDot/master/docs/images/bluedotpython.png
   :height: 246 px
   :width: 274 px
   :scale: 100 %
   :alt: blue dot python client

.. |bluedotpythondevices| image:: https://raw.githubusercontent.com/martinohanlon/BlueDot/master/docs/images/bluedotpythondevices.png
   :height: 247 px
   :width: 506 px
   :scale: 100 %
   :alt: blue dot devices
