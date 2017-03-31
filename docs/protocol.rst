Protocol
========

Blue Dot uses a client/server model, the bluedot Python library starts a bluetooth server, the Blue Dot application connects as a client.

The detail below can be used to create new applications (clients) - if you do please send a pull request :)

bluetooth
---------

Communication over Bluetooth is made using a RFCOMM serial port profile, on port 1, using UUID "00001101-0000-1000-8000-00805f9b34fb".

protocol
--------

The transmission is a 1 way stream between client and server, the server sends no acknowledgements or data to the client.

All messages between client and server conforms to the same format::

    [operation],[x],[y]\n

``operation`` is either 0, 1 or 2:

0. Blue Dot released.
1. Blue Dot pressed.
2. Blue Dot pressed position moved.

``x`` & ``y`` is the position on the Blue Dot where button was pressed, released, moved.

Positions are values between -1 and +1, with 0 being the centre, 1 being the radius of the Blue Dot.

``x`` is the horizontal position, +1 is far right.

``y`` is the vertical position, +1 is the top.

e.g. 

If the blue dot is pressed at the top, the following message would be sent::

    1,0.0,1.0\n

while the blue dot is pressed (held down), the position it is pressed moves to the far right::

    2,1.0,0.0\n

when then button is released::

    0,1.0,0.0\n

If positions cannot be sent, ``x`` and ``y`` should still be sent but be defaulted to ``0``.

Messages should always be terminated with ``\n``.
