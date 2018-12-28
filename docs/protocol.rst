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

The transmission of data from client to server or server to client is a 
simple stream no acknowledgements or data is sent in response to commands.

All messages between conform to the same format::

    [operation],[param1],[param2],[*]\n

Messages are sent when:

Blue Dot is released, pressed or moved - ``[0,1,2],[x],[y]\n``:

    * client to server.

    * *operation*:

        0. Blue Dot released.

        1. Blue Dot pressed.

        2. Blue Dot pressed position moved.

    * *x* & *y* specify the position on the Blue Dot that was pressed, 
    released, and/or moved:

        - Positions are values between -1 and +1, with 0 being the centre and 1 being
            the radius of the Blue Dot.

        - *x* is the horizontal position where +1 is far right.

        - *y* is the vertical position where +1 is the top.

At connection the client sends a handshake - ``[3],[protocol version],[client name]``

    * client to server.

    * *operation* 3.

    * *protocol version* is sent and corresponds to the version of protocol the client supports.

    * *client name* is a string value used in exceptions to report what client has connected.

When the setup (or appearance) of the Blue Dot changes - ``[4],[color],[square],[border],[visible]``:

    * server to client.

    * *operation* 4.

    * *color* a hex value in the format #rrggbbaa representing red, green, blue, alpha values.

    * *square* 0 or 1, 1 if the dot should be a square.

    * *border* 0 or 1, 1 if the dot should have a border.

    * *visible* 0 or 1, 1 if the dot should be visible.

* *\\n* represents the ASCII new-line character (ASCII character 10).

Example
-------

When the Android client connects using protocol version 1::

    3,1,Android Blue Dot app\n

If the blue dot is pressed at the top, the following message will be sent::

    1,0.0,1.0\n

While the blue dot is pressed (held down), the user moves their finger to the
far right causing the following message to be sent::

    2,1.0,0.0\n

The button is then released, resulting in the following message::

    0,1.0,0.0\n

The color of the dot is changed to "red" to server sends to the client::

    4,#ff0000ff,0,0,1\n

Protocol versions
-----------------

0 - initial version
1 - introduction of operation 3, 4