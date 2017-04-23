
Recipes
=======

button
------

The simplest way to use the Blue Dot is as a wireless button.

hello world
~~~~~~~~~~~

When the Blue Dot is pressed, lets say Hello World::

    from bluedot import BlueDot
    bd = BlueDot()
    bd.wait_for_press()
    print("Hello World")

Alternatively you can also use ``when_pressed`` to call a function::

    from bluedot import BlueDot
    from signal import pause

    def say_hello():
        print("Hello World")

    bd = BlueDot()
    bd.when_pressed = say_hello

    pause()

``wait_for_release()`` and ``when_released`` also allow you to interact when the Blue Dot is released::

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

flash an led
~~~~~~~~~~~~

Using Blue Dot in combination with `gpiozero`_ you can interact with electronic components, such as LED's, connected to your Raspberry Pi. 

When the Blue Dot is pressed, the LED will turn on, when released it will turn off::

    from bluedot import BlueDot
    from gpiozero import LED

    bd = BlueDot()
    led = LED(pin)

    bd.wait_for_press()
    led.on()

    bd.wait_for_release()
    led.off()

You could also use ``when_pressed`` and ``when_released``::

    from bluedot import BlueDot
    from gpiozero import LED
    from signal import pause

    bd = BlueDot()
    led = LED(pin)

    bd.when_pressed = led.on
    bd.when_released = led.off

    pause()

Alternatively use ``LED.source`` and ``BlueDot.values``::

    from bluedot import BlueDot
    from gpiozero import LED
    from signal import pause

    bd = BlueDot()
    led = LED(pin)

    led.source = bd.values

    pause()

remote camera
~~~~~~~~~~~~~

Using a Raspberry Pi camera, `picamera`_ and Blue Dot you can really easily create a remote camera::

    from bluedot import BlueDot
    from picamera import PiCamera
    from signal import pause
    
    bd = BlueDot()
    cam = PiCamera()

    def take_picture():
        cam.capture("pic.jpg")

    bd.when_pressed = take_picture

    pause()

joystick
--------

The Blue Dot can also be used as a joystick when the middle, top, bottom, left or right areas of the dot are used.

d pad
~~~~~

Using the position the BlueDot was pressed you can work out whether it was pressed to go up, down, left, right like the dpad on a joystick::

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

    bd = BlueDot()
    bd.when_pressed = dpad

    pause()

At the moment the dpad only registers when it is pressed, to get it work when the position is moved you should add::

    bd.when_moved = dpad

robot
~~~~~

Using the Blue Dot and `gpiozero`_, you can create a bluetooth controlled robot which moves when the dot is pressed and stops when it is released::

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

variable speed robot
~~~~~~~~~~~~~~~~~~~~

You can change the robot to use variable speeds, so the further towards the edge you press the Blue Dot, the faster the robot will go.

``distance`` returns how far from the centre the Blue Dot was pressed, which can be passed to the robot's functions to change its speed::

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

Alternatively you can use a generator and yield ``x``, ``y`` values to Robot's source property (courtesy of `Ben Nuttall`_)::

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

slider
------

By holding down the Blue Dot and moving the position you can use it as an analogue slider.

center out
~~~~~~~~~~

to come

left to right
~~~~~~~~~~~~~

to come

fade an led
~~~~~~~~~~~

to come

bluetooth
---------

You can interact with the Bluetooth adapter using BlueDot.

pairing
~~~~~~~

You can put your raspberry pi into pairing mode which will allow pairing from other devices for 60 seconds::

    from bluedot import BlueDot
    from signal import pause

    bd = BlueDot()
    bd.allow_pairing()

    pause()

Or connect up a physical button up to start the pairing::
    
    from bluedot import BlueDot
    from gpiozero import LED
    from signal import pause

    bd = BlueDot()
    led = LED(pin)

    led.when_pressed = bd.allow_pairing

    pause()

paired devices
~~~~~~~~~~~~~~

You can get the devices that your raspberry pi is paired too::

    from bluedot import BlueDot
    bd = BlueDot()
    
    devices = bd.adapter.paired_devices
    for d in devices:
        device_address = d[0]
        device_name = d[1]

testing
-------

bluedot includes a MockBlueDot class to allow you to test and debug your program without having to use bluetooth or a Blue Dot client.

MockBlueDot inherits from BlueDot and is used in the same way, but you have the option of launching a mock app which you can click with a mouse or writing scripts to simulate the Blue Dot being used.

|mockbluedot|

The mock app uses pygame, which is installed with Raspbian, but you can install using::

    sudo apt-get install python3-pygame

Or if you are using Python 2 ::

    sudo apt-get install python-pygame

mock app
~~~~~~~~

Launch the mock Blue Dot app to test by clicking the on-screen dot with the mouse::

    from bluedot import MockBlueDot
    from signal import pause

    def say_hello():
        print("Hello World")

    bd = MockBlueDot()
    bd.when_pressed = say_hello

    bd.launch_mock_app()
    pause()

scripted tests
~~~~~~~~~~~~~~

Tests can also be scripted using MockBlueDot::

    from bluedot import MockBlueDot

    def say_hello():
        print("Hello World")

    bd = MockBlueDot()
    bd.when_pressed = say_hello

    bd.mock_blue_dot_pressed(0,0)

.. _gpiozero: https://gpiozero.readthedocs.io
.. _picamera: https://picamera.readthedocs.io
.. _Ben Nuttall: https://github.com/bennuttall

.. |mockbluedot| image:: images/mockbluedot.png
   :alt: mock blue dot app
