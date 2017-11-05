Blue Dot Python App
===================

Blue Dot Python app allows you to use another Raspberry Pi (or linux based computer) as the Blue Dot remote.

|bluedotpython| |bluedotpythondevices|

Start
-----

The app is included in the bluedot Python library:

1. If you havent already done so, pair your raspberry pi and install the Python library as described in the `getting started`_ guide
2. Run the Blue Dot app::

    python3 -m bluedot.app

4. Select your Raspberry Pi from the paired devices list

|bluedotpythondevices|

5. Press the Dot 

|bluedotpython|

Options
-------

To get help with the Blue Dot app options::

    python3 -m bluedot.app --help

If you have more than 1 bluetooth device you can use ``--device`` to use a particular device::

    python3 -m bluedot.app --device hci1

You can specify the server to connect to at startup by using the ``--server`` option::

    python3 -m bluedot.app --server myraspberrypi

The screen size of the Blue Dot app can be changed using the ``width`` and ``height`` options and specifying the number of pixels::

    python3 -m bluedot.app --width 500 -- height 500

The app can also be used full screen, if no ``width`` or ``height`` is given the screen will be sized to the current resolution of the screen::

    python3 -m bluedot.app --fullscreen

.. _getting started: http://bluedot.readthedocs.io/en/latest/gettingstarted.html

.. |bluedotpython| image:: https://raw.githubusercontent.com/martinohanlon/BlueDot/master/docs/images/bluedotpython.png
   :height: 274 px
   :width: 324 px
   :scale: 100 %
   :alt: blue dot python app

.. |bluedotpythondevices| image:: https://raw.githubusercontent.com/martinohanlon/BlueDot/master/docs/images/bluedotpythondevices.png
   :height: 273 px
   :width: 326 px
   :scale: 100 %
   :alt: blue dot devices
