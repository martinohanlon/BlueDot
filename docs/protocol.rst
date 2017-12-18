Protocol
========

Blue Dot uses a client/server model. The :class:`BlueDot` class starts a
Bluetooth server, the Blue Dot application connects as a client.

The detail below can be used to create new applications (clients); if you do
please send a pull request :)

Bluetooth
---------

Communication over Bluetooth is made using a RFCOMM serial port profile, on
port 1, using UUID "00001101-0000-1000-8000-00805f9b34fb".

Specification
-------------

The transmission is a 1-way stream from client to server; the server sends
no acknowledgements or data back to the client.

All messages between client and server conform to the same format::

    [operation],[x],[y]\n

Where:

* *operation* is either 0, 1 or 2:

   - Blue Dot released.

   - Blue Dot pressed.

   - Blue Dot pressed position moved.

* *x* & *y* specify the position on the Blue Dot that was pressed,
  released, and/or moved.

  - Positions are values between -1 and +1, with 0 being the centre and 1 being
    the radius of the Blue Dot.

  - *x* is the horizontal position where +1 is far right.

  - *y* is the vertical position where +1 is the top.

* *\\n* represents the ASCII new-line character (ASCII character 10).

Example
-------

If the blue dot is pressed at the top, the following message will be sent::

    1,0.0,1.0\n

While the blue dot is pressed (held down), the user moves their finger to the
far right causing the following message to be sent::

    2,1.0,0.0\n

The button is then released, resulting in the following message::

    0,1.0,0.0\n

If positions cannot be sent, *x* and *y* will still be sent but will default to
0.
