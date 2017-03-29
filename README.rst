Blue Dot
========

Blue Dot allows you to control your Raspberry Pi projects wirelessly - its a bluetooth remote and zero boiler plate (super simple to use :) Python library.

|bluedotapp|

Created by `Martin O'Hanlon`_, `@martinohanlon`_, `stuffaboutco.de`_.

start
-----

Getting started is really simple:

1. Download the `Blue Dot app`_
2. Pair your Raspberry Pi to your Bluetooth device
3. Install the Python library
4. Write some code::

    from bluedot import BlueDot
    dot = BlueDot()
    dot.wait_for_press()
    print("You pressed the blue dot!")

5. Press the Blue Dot

See the `getting started`_ guide to 'get started'!

more
----

The Blue Dot is a joystick as well as button, you can tell if the dot was pressed in the middle, on the top, bottom, left or right.

Why be restricted by such vague positions like top and bottom though, you can get the exact x, y position or even the angle and distance from centre where the dot was pressed.

Its not all about when the button was pressed either - pressed, released or moved they all work.

One blue circle can do a lot.

even more
---------

The `online documentation`_ describes how to use Blue Dot and the Python library, be sure to also check out the `examples`_.

status
------

Alpha - it works, but expect rough edges and future changes which break compatability.


.. _Martin O'Hanlon: https://github.com/martinohanlon
.. _stuffaboutco.de: https://stuffaboutco.de
.. _@martinohanlon: https://twitter.com/martinohanlon
.. _getting started: http://bluedot.readthedocs.io/en/latest/gettingstarted.html
.. _online documentation: <http://bluedot.readthedocs.io/en/latest/
.. _examples: https://github.com/martinohanlon/BlueDot/tree/master/examples
.. _Blue Dot app: https://github.com/martinohanlon/BlueDot/blob/android-dev/clients/android/app/app-release.apk?raw=true

.. |bluedotapp| image:: https://raw.githubusercontent.com/martinohanlon/BlueDot/master/docs/images/bluedotandroid.png
   :height: 1231 px
   :width: 719 px
   :scale: 20 %
   :alt: blue dot app