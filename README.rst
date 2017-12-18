Blue Dot
========

|pypibadge| |docsbadge|

Blue Dot allows you to control your Raspberry Pi projects wirelessly - it's a Bluetooth remote and zero boiler plate (super simple to use :) Python library.

|bluedotfeature|

|bluedotapp| |bluedotpython|

Created by `Martin O'Hanlon`_ (`@martinohanlon`_, `stuffaboutco.de`_).

Getting Started
---------------

`Install and usage`_ is really simple:

1. Install the Python library::

       sudo pip3 install bluedot

2. Get the `Android Blue Dot app`_ or use the `Python Blue Dot app`_

3. Pair your Raspberry Pi

4. Write some code::

       from bluedot import BlueDot
       bd = BlueDot()
       bd.wait_for_press()
       print("You pressed the blue dot!")

5. Press the Blue Dot

See the `getting started`_ guide to 'get statred'!

More
----

The Blue Dot is a `joystick`_ as well as `button`_. You can tell if the dot was pressed in the middle, on the top, bottom, left or right. You can easily create a `BlueDot controlled Robot`_.

Why be restricted by such vague positions like top and bottom though: you can get the exact (x, y) position or even the angle and distance from centre where the dot was pressed.

Its not all about when the button was pressed either - pressed, released or moved they all work.

You can press it, `slide it`_, `swipe it`_, `rotate it`_ - one blue circle can do a lot!

Even more
---------

The `online documentation`_ describes how to use Blue Dot and the `Python library`_ including `Recipes`_ and ideas.

Status
------

Production - under active development. Be sure to raise an `issue`_ if you have a feature request or experience problems.

.. _Martin O'Hanlon: https://github.com/martinohanlon
.. _stuffaboutco.de: http://stuffaboutco.de
.. _@martinohanlon: https://twitter.com/martinohanlon
.. _getting started: http://bluedot.readthedocs.io/en/latest/gettingstarted.html
.. _Install and usage: http://bluedot.readthedocs.io/en/latest/gettingstarted.html
.. _online documentation: http://bluedot.readthedocs.io/en/latest/
.. _Python library: http://bluedot.readthedocs.io/en/latest/dotapi.html
.. _examples: https://github.com/martinohanlon/BlueDot/tree/master/examples
.. _Recipes: http://bluedot.readthedocs.io/en/latest/recipes.html
.. _Android Blue Dot app: http://play.google.com/store/apps/details?id=com.stuffaboutcode.bluedot
.. _Python Blue Dot app: http://bluedot.readthedocs.io/en/latest/bluedotpythonapp.html
.. _issue: https://github.com/martinohanlon/bluedot/issues
.. _BlueDot controlled Robot: https://youtu.be/eW9oEPySF58
.. _joystick: http://bluedot.readthedocs.io/en/latest/recipes.html#joystick
.. _button: http://bluedot.readthedocs.io/en/latest/recipes.html#button
.. _slide it: http://bluedot.readthedocs.io/en/latest/recipes.html#slider
.. _swipe it: http://bluedot.readthedocs.io/en/latest/recipes.html#swiping
.. _rotate it: http://bluedot.readthedocs.io/en/latest/recipes.html#rotating

.. |bluedotapp| image:: https://raw.githubusercontent.com/martinohanlon/BlueDot/master/docs/images/bluedotandroid_small.png
   :height: 247 px
   :width: 144 px
   :scale: 100 %
   :alt: blue dot app

.. |bluedotpython| image:: https://raw.githubusercontent.com/martinohanlon/BlueDot/master/docs/images/bluedotpython.png
   :height: 247 px
   :width: 294 px
   :scale: 100 %
   :alt: blue dot python app

.. |bluedotfeature| image:: https://raw.githubusercontent.com/martinohanlon/BlueDot/master/docs/images/blue_dot_feature_small.png
   :height: 247 px
   :width: 506 px
   :scale: 100 %
   :alt: blue dot feature

.. |pypibadge| image:: https://badge.fury.io/py/bluedot.svg
   :target: https://badge.fury.io/py/bluedot
   :alt: Latest Version

.. |docsbadge| image:: https://readthedocs.org/projects/bluedot/badge/
   :target: https://readthedocs.org/projects/bluedot/
   :alt: Docs
