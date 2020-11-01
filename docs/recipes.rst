Recipes
=======

The recipes provide examples of how you can use Blue Dot. Don't be restricted
by these ideas and be sure to have a look at the :doc:`dotapi` as there is more
to be discovered.

Button
------

The simplest way to use the Blue Dot is as a wireless button.

Hello World
~~~~~~~~~~~

.. currentmodule:: bluedot

Let's say "Hello World" by creating the :class:`BlueDot` object then waiting
for the Blue Dot app to connect and the button be pressed:

.. literalinclude:: examples/hello_world.py

Alternatively you can also use :attr:`~BlueDot.when_pressed` to call a
function:

.. literalinclude:: examples/hello_event.py

:attr:`~BlueDot.wait_for_release` and :attr:`~BlueDot.when_released` also allow
you to interact when the button is released:

.. literalinclude:: examples/goodbye_world.py

Double presses can also be used with :attr:`~BlueDot.wait_for_double_press` and
:attr:`~BlueDot.when_double_pressed`:

.. literalinclude:: examples/shout_hello.py

Flash an LED
~~~~~~~~~~~~

Using Blue Dot in combination with :mod:`gpiozero` you can interact with
electronic components, such as LEDs, connected to your Raspberry Pi.

When a button is pressed, the LED connected to GPIO 27 will turn on; when
released it will turn off:

.. literalinclude:: examples/led1.py

You could also use :attr:`~BlueDot.when_pressed` and
:attr:`~BlueDot.when_released`:

.. literalinclude:: examples/led2.py

Alternatively use :attr:`~gpiozero.SourceMixin.source` and
:attr:`~BlueDot.values`:

.. literalinclude:: examples/led3.py

Remote Camera
~~~~~~~~~~~~~

Using a Raspberry Pi camera module, :class:`picamera.PiCamera` and
:class:`BlueDot`, you can really easily create a remote camera:

.. literalinclude:: examples/camera.py

Joystick
--------

The Blue Dot can also be used as a joystick when the middle, top, bottom, left
or right areas of the dot are touched.

D-pad
~~~~~

Using the position the Blue Dot was pressed you can work out whether it was
pressed to go up, down, left, right like the `D-pad`_ on a joystick:

.. literalinclude:: examples/dpad.py

At the moment the `D-pad`_ only registers when it is pressed. To get it work
when the position is moved you should add the following line above
:code:`pause()`::

    bd.when_moved = dpad

Robot
~~~~~

These recipes assume your robot is constructed with a pair of H-bridges. The
forward and backward pins for the H-bridge of the left wheel are 17 and 18
respectively, and the forward and backward pins for H-bridge of the right wheel
are 22 and 23 respectively.

Using the Blue Dot and :class:`gpiozero.Robot`, you can create a `bluetooth
controlled robot`_ which moves when the dot is pressed and stops when it is
released:

.. literalinclude:: examples/robot1.py

Variable Speed Robot
~~~~~~~~~~~~~~~~~~~~

You can change the robot to use variable speeds, so the further towards the
edge you press the Blue Dot, the faster the robot will go.

The :attr:`~BlueDotPosition.distance` attribute returns how far from the centre
the Blue Dot was pressed, which can be passed to the robot's functions to
change its speed:

.. literalinclude:: examples/robot2.py

Alternatively you can use a generator and yield (x, y) values to the
:attr:`gpiozero.Robot.source` property (courtesy of `Ben Nuttall`_):

.. literalinclude:: examples/robot3.py

Appearance
----------

The button doesn't have to be blue or a dot, you can change how it looks, or make it completely invisible.

.. image:: images/bluedot_color_changing_smaller.gif
   :alt: Animation of blue dot app cycling through colors and changing to a square

Colo(u)r
~~~~~~~~

To change the color of the button use the :attr:`~BlueDot.color`: property:

.. literalinclude:: examples/looks_color.py

A dictionary of available colors can be obtained from ``bluedot.COLORS``.

The color can also be set using a hex value of `#rrggbb` or `#rrggbbaa` value::

    bd.color = "#00ff00"

Or a tuple of 3 or 4 integers between `0` and `255` either (red, gree, blue) or (red, green, blue, alpha)::

    bd.color = (0, 255, 0)

Square
~~~~~~

The button can also be made square using the :attr:`~BlueDot.square`: property:

.. literalinclude:: examples/looks_square.py

Border
~~~~~~

A border can also been added to the button by setting the :attr:`~BlueDot.border`: property to `True`:

.. literalinclude:: examples/looks_border.py

(In)visible
~~~~~~~~~~~

The button can be hidden and shown using the :attr:`~BlueDot.visible`: property:

.. literalinclude:: examples/looks_visible.py

Layout
-------

You can have as many buttons as you want.

The Buttons need to be in a grid of columns and rows.

.. image:: images/layout_many_buttons_small.png
   :alt: Android blue dot app showing 10 buttons in a 2x5 grid

By hiding specific buttons and being creative with the button's appearance you can create very sophisticated layouts for your controllers using Blue Dot.

.. image:: images/layout_joypad_small.png
   :alt: Android blue dot app showing buttons layed out like a classic joypad

The Blue Dot android app supports multi touch allowing you to use multiple buttons simultaneously

.. note::

    Currently only the Android client app supports multi buttons.

Two Buttons
~~~~~~~~~~~

Create 2 buttons side by side, by setting the number of `cols` to `2`:

.. image:: images/layout_2_buttons_small.png
   :alt: Android blue dot app showing 2 buttons side by side

.. literalinclude:: examples/two_buttons.py

The buttons could be made verticle by setting the `rows` attribute::

    bd = BlueDot(rows=2)

Each button can be set to call its own function by using the grid position:

.. literalinclude:: examples/two_buttons_two_events.py

To create a gap in between the buttons you could create a row of 3 buttons and hide the middle button:

.. image:: images/layout_2_buttons_gap_small.png
   :alt: Android blue dot app showing 2 buttons side by side with a gap in the middle

.. literalinclude:: examples/two_buttons_gap.py

Many Buttons
~~~~~~~~~~~~

Create a grid of buttons by setting the `cols` and `rows` e.g. 10 buttons in a 2x5 grid:

.. image:: images/layout_many_buttons_small.png
   :alt: Android blue dot app showing 10 buttons in a 2x5 grid

.. literalinclude:: examples/many_buttons.py

You could assign all the buttons random colors:

.. literalinclude:: examples/many_buttons_random_colors.py

D-pad
~~~~~

Create a traditional d-pad layout by using a 3x3 grid and hide the buttons at the corners and in the middle:

.. image:: images/layout_dpad_small.png
   :alt: Android blue dot app showing 4 buttons arranged in a cross

.. literalinclude:: examples/dpad_layout.py

Add 2 buttons on the right to create a joypad:

.. image:: images/layout_joypad_small.png
   :alt: Android blue dot app showing buttons layed out like a classic joypad

.. literalinclude:: examples/dpad_layout.py

Slider
------

By holding down a button and moving the position you can use it as an
analogue slider.

Centre Out
~~~~~~~~~~

Using the :attr:`BlueDotPosition.distance` property which is returned when the
position is moved you can create a slider which goes from the centre out in any
direction:

.. literalinclude:: examples/slider_centre.py

Left to Right
~~~~~~~~~~~~~

The :attr:`BlueDotPosition.x` property returns a value from -1 (far left) to 1
(far right). Using this value you can create a slider which goes horizontally
through the middle:

.. literalinclude:: examples/slider_left_right.py

To make a vertical slider you could change the code above to use
:attr:`BlueDotPosition.y` instead.

Dimmer Switch
~~~~~~~~~~~~~

Using the :class:`gpiozero.PWMLED` class and :class:`BlueDot` as a vertical
slider you can create a wireless dimmer switch:

.. literalinclude:: examples/slider_dimmer.py

Swiping
-------

You can interact with the Blue Dot by swiping across it, like you would to move
between pages in a mobile app.

Single
~~~~~~

Detecting a single swipe is easy using :attr:`~BlueDot.wait_for_swipe`:

.. literalinclude:: examples/swipe1.py

Alternatively you can also use :attr:`~BlueDot.when_swiped` to call a
function:

.. literalinclude:: examples/swipe2.py

Direction
~~~~~~~~~

You can tell what direction the Blue Dot is swiped by using the
:class:`BlueDotSwipe` object passed to the function assigned to
:attr:`~BlueDot.when_swiped`:

.. literalinclude:: examples/swipe_direction.py

Speed, Angle, and Distance
~~~~~~~~~~~~~~~~~~~~~~~~~~

:class:`BlueDotSwipe` returns more than just the direction. It also includes
the speed of the swipe (in Blue Dot radius per second), the angle, and the
distance between the start and end positions of the swipe:

.. literalinclude:: examples/swipe_speed_angle.py

Rotating
--------

You can use Blue Dot like a rotary encoder or "iPod classic click wheel" -
rotating around the outer edge of the Blue Dot will cause it to "tick".  The
Blue Dot is split into a number of virtual segments (the default is 8), when
the position moves from one segment to another, it ticks.

Counter
~~~~~~~

Using the :attr:`~BlueDot.when_rotated` callback you can create a counter which
increments / decrements when the Blue Dot is rotated either clockwise or
anti-clockwise. A :class:`BlueDotRotation` object is passed to the callback.
Its :attr:`~BlueDotRotation.value` property will be -1 if rotated
anti-clockwise and 1 if rotated clockwise:

.. literalinclude:: examples/rotation.py

The rotation speed can be modified using the :attr:`BlueDot.rotation_segments`
property which changes the number of segments the Blue Dot is split into::

    bd.rotation_segments = 16

Multiple Blue Dot Apps
----------------------

You can connect multiple Blue Dot clients (apps) to a single server (python 
program) by using different Bluetooth ports for each app.

Create multiple `BlueDot` servers using specific ports:

.. literalinclude:: examples/multiple_dots.py

Change the BlueDot app to use the specific port by:

1. Opening settings from the menu
2. Turning *Auto port discovery* off
3. Selecting the specific *Bluetooth port*

.. image:: images/bluedotandroid_settings.png
   :alt: Android blue dot app showing the settings option on the menu

.. image:: images/bluedotandroid_settings_autoport.png
   :alt: Android blue dot app showing the settings page and auto port discovery turned on

.. image:: images/bluedotandroid_settings_port.png
   :alt: Android blue dot app showing the settings page, auto port discovery turned off and bluetooth port 1 selected

Bluetooth
---------

You can interact with the Bluetooth adapter using :class:`BlueDot`.

Pairing
~~~~~~~

You can put your Raspberry Pi into pairing mode which will allow pairing from
other devices for 60 seconds:

.. literalinclude:: examples/bt_pairing.py

Or connect up a physical button up to start the pairing (the button is assumed
to be wired to GPIO 27):

.. literalinclude:: examples/bt_pair_button.py

Paired Devices
~~~~~~~~~~~~~~

You can iterate over the devices that your Raspberry Pi is paired too:

.. literalinclude:: examples/bt_enumerate.py

Testing
-------

Blue Dot includes a :class:`MockBlueDot` class to allow you to test and debug
your program without having to use Bluetooth or a Blue Dot client.

:class:`MockBlueDot` inherits from :class:`BlueDot` and is used in the same
way, but you have the option of launching a mock app which you can click with a
mouse or writing scripts to simulate the Blue Dot being used.

.. image:: images/mockbluedot.png
   :alt: Screenshot of the mock Blue Dot app

Mock App
~~~~~~~~

Launch the mock Blue Dot app to test by clicking the on-screen dot with the
mouse:

.. literalinclude:: examples/mock_app.py

Scripted Tests
~~~~~~~~~~~~~~

Tests can also be scripted using :class:`MockBlueDot`:

.. literalinclude:: examples/mock_script.py


.. _Ben Nuttall: https://github.com/bennuttall
.. _bluetooth controlled robot: https://youtu.be/eW9oEPySF58
.. _D-pad: https://en.wikipedia.org/wiki/D-pad
