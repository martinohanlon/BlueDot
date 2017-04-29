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

You can specify the server to connect to at startup by using the ``--server`` option::

    python3 -m bluedot.client --server myraspberrypi

To start the client in full screen mode use::

    python3 -m bluedot.client --fullscreen

If you have more than 1 bluetooth device you can use ``--device`` to use a particular device::

    python3 -m bluedot.client --device hci0


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
