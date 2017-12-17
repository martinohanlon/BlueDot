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
for the Blue Dot app to connect and be pressed::

    from bluedot import BlueDot
    bd = BlueDot()
    bd.wait_for_press()
    print("Hello World")

Alternatively you can also use :attr:`~BlueDot.when_pressed` to call a
function::

    from bluedot import BlueDot
    from signal import pause

    def say_hello():
        print("Hello World")

    bd = BlueDot()
    bd.when_pressed = say_hello

    pause()

:attr:`~BlueDot.wait_for_release` and :attr:`~BlueDot.when_released` also allow
you to interact when the Blue Dot is released::

    from bluedot import BlueDot
    from signal import pause

    def say_hello():
        print("Hello World")

    def say_goodbye():
        print("goodbye")

    bd = BlueDot()
    bd.when_pressed = say_hello
    bd.when_released = say_goodbye

    pause()

Double presses can also be used with :attr:`~BlueDot.wait_for_double_press` and
:attr:`~BlueDot.when_double_pressed`::

    from bluedot import BlueDot
    from signal import pause

    def shout_hello():
        print("HELLO")

    bd = BlueDot()
    bd.when_double_pressed = shout_hello

    pause()

Flash an LED
~~~~~~~~~~~~

Using Blue Dot in combination with :mod:`gpiozero` you can interact with
electronic components, such as LEDs, connected to your Raspberry Pi.

When the Blue Dot is pressed, the LED will turn on; when released it will turn
off::

    from bluedot import BlueDot
    from gpiozero import LED

    bd = BlueDot()
    led = LED(pin)

    bd.wait_for_press()
    led.on()

    bd.wait_for_release()
    led.off()

You could also use :attr:`~BlueDot.when_pressed` and
:attr:`~BlueDot.when_released`::

    from bluedot import BlueDot
    from gpiozero import LED
    from signal import pause

    bd = BlueDot()
    led = LED(pin)

    bd.when_pressed = led.on
    bd.when_released = led.off

    pause()

Alternatively use :attr:`~gpiozero.SourceMixin.source` and
:attr:`~BlueDot.values`::

    from bluedot import BlueDot
    from gpiozero import LED
    from signal import pause

    bd = BlueDot()
    led = LED(pin)

    led.source = bd.values

    pause()

Remote Camera
~~~~~~~~~~~~~

Using a Raspberry Pi camera module, :class:`picamera.PiCamera` and
:class:`BlueDot`, you can really easily create a remote camera::

    from bluedot import BlueDot
    from picamera import PiCamera
    from signal import pause

    bd = BlueDot()
    cam = PiCamera()

    def take_picture():
        cam.capture("pic.jpg")

    bd.when_pressed = take_picture

    pause()

Joystick
--------

The Blue Dot can also be used as a joystick when the middle, top, bottom, left
or right areas of the dot are touched.

D-pad
~~~~~

Using the position the Blue Dot was pressed you can work out whether it was
pressed to go up, down, left, right like the `D-pad`_ on a joystick::

    from bluedot import BlueDot
    from signal import pause

    def dpad(pos):
        if pos.top:
            print("up")
        elif pos.bottom:
            print("down")
        elif pos.left:
            print("left")
        elif pos.right:
            print("right")
        elif pos.middle:
            print("fire")

    bd = BlueDot()
    bd.when_pressed = dpad

    pause()

At the moment the `D-pad`_ only registers when it is pressed. To get it work
when the position is moved you should add the following line above
:code:`pause`::

    bd.when_moved = dpad

Robot
~~~~~

Using the Blue Dot and :class:`gpiozero.Robot`, you can create a `bluetooth
controlled robot`_ which moves when the dot is pressed and stops when it is
released::

    from bluedot import BlueDot
    from gpiozero import Robot
    from signal import pause

    bd = BlueDot()
    robot = Robot(left=(lfpin, lbpin), right=(rfpin, rbpin))

    def move(pos):
        if pos.top:
            robot.forward()
        elif pos.bottom:
            robot.backward()
        elif pos.left:
            robot.left()
        elif pos.right:
            robot.right()

    def stop():
        robot.stop()

    bd.when_pressed = move
    bd.when_moved = move
    bd.when_released = stop

    pause()

Variable Speed Robot
~~~~~~~~~~~~~~~~~~~~

You can change the robot to use variable speeds, so the further towards the
edge you press the Blue Dot, the faster the robot will go.

The :attr:`~BlueDotPosition.distance` attribute returns how far from the centre
the Blue Dot was pressed, which can be passed to the robot's functions to
change its speed::

    from bluedot import BlueDot
    from gpiozero import Robot
    from signal import pause

    bd = BlueDot()
    robot = Robot(left=(lfpin, lbpin), right=(rfpin, rbpin))

    def move(pos):
        if pos.top:
            robot.forward(pos.distance)
        elif pos.bottom:
            robot.backward(pos.distance)
        elif pos.left:
            robot.left(pos.distance)
        elif pos.right:
            robot.right(pos.distance)

    def stop():
        robot.stop()

    bd.when_pressed = move
    bd.when_moved = move
    bd.when_released = stop

    pause()

Alternatively you can use a generator and yield (x, y) values to the
:attr:`gpiozero.Robot.source` property (courtesy of `Ben Nuttall`_)::

    from gpiozero import Robot
    from bluedot import BlueDot
    from signal import pause

    def pos_to_values(x, y):
        left = y if x > 0 else y + x
        right = y if x < 0 else y - x
        return (clamped(left), clamped(right))

    def clamped(v):
        return max(-1, min(1, v))

    def drive():
        while True:
            if bd.is_pressed:
                x, y = bd.position.x, bd.position.y
                yield pos_to_values(x, y)
            else:
                yield (0, 0)

    robot = Robot(left=(lfpin, lbpin), right=(rfpin, rbpin))
    bd = BlueDot()

    robot.source = drive()

    pause()

Slider
------

By holding down the Blue Dot and moving the position you can use it as an
analogue slider.

Centre Out
~~~~~~~~~~

Using the :attr:`BlueDotPosition.distance` property which is returned when the
position is moved you can create a slider which goes from the centre out in any
direction::

    from bluedot import BlueDot
    from signal import pause

    def show_percentage(pos):
        percentage = round(pos.distance * 100, 2)
        print("{}%".format(percentage))

    bd = BlueDot()
    bd.when_moved = show_percentage

    pause()

Left to Right
~~~~~~~~~~~~~

The :attr:`BlueDotPosition.x` property returns a value from -1 (far left) to 1
(far right). Using this value you can create a slider which goes horizontally
through the middle::

    from bluedot import BlueDot
    from signal import pause

    def show_percentage(pos):
        horizontal = ((pos.x + 1) / 2)
        percentage = round(horizontal * 100, 2)
        print("{}%".format(percentage))

    bd = BlueDot()
    bd.when_moved = show_percentage

    pause()

To make a vertical slider you could change the code above to use
:attr:`BlueDotPosition.y` instead.

Dimmer Switch
~~~~~~~~~~~~~

Using the :class:`gpiozero.PWMLED` class and :class:`BlueDot` as a vertical
slider you can create a wireless dimmer switch::

    from bluedot import BlueDot
    from gpiozero import PWMLED
    from signal import pause

    def set_brightness(pos):
        brightness = ((pos.y + 1) / 2)
        led.value = brightness

    bd = BlueDot()
    bd.when_moved = set_brightness
    led = PWMLED(pin)

    pause()

Swiping
-------

You can interact with the Blue Dot by swiping across it, like you would to move
between pages in a mobile app.

Single
~~~~~~

Detecting a single swipe is easy using :attr:`~BlueDot.wait_for_swipe`::

    from bluedot import BlueDot
    bd = BlueDot()
    bd.wait_for_swipe()
    print("Blue Dot swiped")

Alternatively you can also use :attr:`~BlueDot.when_swiped` to call a
function::

    from bluedot import BlueDot
    from signal import pause

    def swiped():
        print("Blue Dot swiped")

    bd = BlueDot()
    bd.when_swiped = swiped

    pause()

Direction
~~~~~~~~~

You can tell what direction the Blue Dot is swiped by using the
:class:`BlueDotSwipe` object passed to the function assigned to
:attr:`~BlueDot.when_swiped`::

    from bluedot import BlueDot
    from signal import pause

    def swiped(swipe):
        if swipe.up:
            print("up")
        elif swipe.down:
            print("down")
        elif swipe.left:
            print("left")
        elif swipe.right:
            print("right")

    bd = BlueDot()
    bd.when_swiped = swiped

    pause()

Speed, Angle, and Distance
~~~~~~~~~~~~~~~~~~~~~~~~~~

:class:`BlueDotSwipe` returns more than just the direction. It also includes
the speed of the swipe (in Blue Dot radius per second), the angle, and the
distance between the start and end positions of the swipe::

    from bluedot import BlueDot
    from signal import pause

    def swiped(swipe):
        print("Swiped")
        print("speed={}".format(swipe.speed))
        print("angle={}".format(swipe.angle))
        print("distance={}".format(swipe.distance))

    bd = BlueDot()
    bd.when_swiped = swiped

    pause()

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
anti-clockwise and 1 if rotated clockwise::

    from bluedot import BlueDot
    from signal import pause

    count = 0

    def rotated(rotation):
        global count
        count += rotation.value

        print("{} {} {}".format(count,
                                rotation.clockwise,
                                rotation.anti_clockwise))

    bd = BlueDot()
    bd.when_rotated = rotated

    pause()

The rotation speed can be modified using the :attr:`BlueDot.rotation_segments`
property which changes the number of segments the Blue Dot is split into::

    bd.rotation_segments = 16

Bluetooth
---------

You can interact with the Bluetooth adapter using :class:`BlueDot`.

Pairing
~~~~~~~

You can put your Raspberry Pi into pairing mode which will allow pairing from
other devices for 60 seconds::

    from bluedot import BlueDot
    from signal import pause

    bd = BlueDot()
    bd.allow_pairing()

    pause()

Or connect up a physical button up to start the pairing::

    from bluedot import BlueDot
    from gpiozero import Button
    from signal import pause

    bd = BlueDot()
    button = Button(pin)

    button.when_pressed = bd.allow_pairing

    pause()

Paired Devices
~~~~~~~~~~~~~~

You can iterate over the devices that your Raspberry Pi is paired too::

    from bluedot import BlueDot
    bd = BlueDot()

    devices = bd.paired_devices
    for d in devices:
        device_address = d[0]
        device_name = d[1]

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
mouse::

    from bluedot import MockBlueDot
    from signal import pause

    def say_hello():
        print("Hello World")

    bd = MockBlueDot()
    bd.when_pressed = say_hello

    bd.launch_mock_app()
    pause()

Scripted Tests
~~~~~~~~~~~~~~

Tests can also be scripted using :class:`MockBlueDot`::

    from bluedot import MockBlueDot

    def say_hello():
        print("Hello World")

    bd = MockBlueDot()
    bd.when_pressed = say_hello

    bd.mock_client_connected()
    bd.mock_blue_dot_pressed(0,0)

.. _Ben Nuttall: https://github.com/bennuttall
.. _bluetooth controlled robot: https://youtu.be/eW9oEPySF58
.. _D-pad: https://en.wikipedia.org/wiki/D-pad
