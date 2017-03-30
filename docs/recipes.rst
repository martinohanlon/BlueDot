
Recipes
=======

button
------

The simplest way to use the Blue Dot is as a wireless button.

hello world
~~~~~~~~~~~

When the Blue Dot is pressed, lets say Hello World::

    from bluedot import BlueDot
    dot = BlueDot()
    dot.wait_for_press()
    print("Hello World")

Alternatively you can also use ``when_pressed`` to call a function::

    from bluedot import BlueDot

    def say_hello():
        print("Hello World")

    dot = BlueDot()
    dot.when_pressed = say_hello

``wait_for_release()`` and ``when_released`` also allow you to interact when the Blue Dot is released::

    from bluedot import BlueDot

    def say_hello():
        print("Hello World")

    def say_goodbye():
        print("goodbye")

    dot = BlueDot()
    dot.when_pressed = say_hello
    dot.when_released = say_goodbye

flash an led
~~~~~~~~~~~~

Using Blue Dot in combination with `gpiozero`_ you can interact with electronic components, such as LED's, connected to your Raspberry Pi. 

When the Blue Dot is pressed, the LED will turn on, when released it will turn off::

    from bluedot import BlueDot
    from gpiozero import LED

    dot = BlueDot()
    led = LED(pin)

    dot.wait_for_press()
    led.on()

    dot.wait_for_release()
    led.off()

Alternatively::

    from bluedot import BlueDot
    from gpiozero import LED

    dot = BlueDot()
    led = LED(pin)

    dot.when_pressed = led.on

    dot.when_released = led.off

remote camera
~~~~~~~~~~~~~

Using a Raspberry Pi camera, `picamera`_ and Blue Dot you can really easily create a remote camera ::

    from bluedot import BlueDot
    from picamera import PiCamera
    
    dot = BlueDot()
    cam = PiCamera()

    def take_picture():
        cam.capture("pic.jpg")

    dot.when_pressed = take_picture

joystick
--------

The Blue Dot can also be used as a joystick when the middle, top, bottom, left or right areas of the dot are used.

d pad
~~~~~

to come

robot
~~~~~

to come

variable speed robot
~~~~~~~~~~~~~~~~~~~~

to come

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


.. _gpiozero: https://gpiozero.readthedocs.io
.. _picamera: https://picamera.readthedocs.io
