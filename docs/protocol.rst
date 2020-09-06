Protocol
========

Blue Dot uses a client/server model. The :class:`BlueDot` class starts a
Bluetooth server, the Blue Dot application connects as a client.

The detail below can be used to create new applications (clients); if you do
please send a pull request :)

Bluetooth
---------

Communication over Bluetooth is made using a RFCOMM serial port profile using 
UUID "00001101-0000-1000-8000-00805f9b34fb".

Specification
-------------

The transmission of data from client to server or server to client is a 
simple stream no acknowledgements or data is sent in response to commands.

All messages between conform to the same format::

    [operation],[param1],[param2],[*]\n

Messages are sent when:

1. A client connects
3. When the setup (or appearance) of a button changes
2. A button is released, pressed or moved

At connection the client sends a handshake - ``[3],[protocol version],[client name]\n``

* client to server.

* *operation* 3.

* *protocol version* is sent and corresponds to the version of protocol the client supports.

* *client name* is a string value used in exceptions to report what client has connected.

At connection or when the default setup (or appearance) changes - ``[4],[color],[square],[border],[visible],[cols],[rows]\n``:

* server to client.

* *operation* 4.

* set the values of the all the buttons

* *color* is a hex value in the format #rrggbbaa representing red, green, blue, alpha values.

* *square* is 0 or 1, 1 if the dot should be a square.

* *border* is 0 or 1, 1 if the dot should have a border.

* *visible* is 0 or 1, 1 if the dot should be visible.

* *cols* is the number of columns in the matrix of buttons

* *rows* is the number of columns in the matrix of buttons

When the appearance of a button changes from the default - - ``[5],[color],[square],[border],[visible],[col],[row]\n``:

* server to client.

* *operation* 5.

* *color* is a hex value in the format #rrggbbaa representing red, green, blue, alpha values.

* *square* is 0 or 1, 1 if the dot should be a square.

* *border* is 0 or 1, 1 if the dot should have a border.

* *visible* is 0 or 1, 1 if the dot should be visible.

* *col* and *row* specify the button's position in the matrix 

When a button is released, pressed or moved - ``[0,1,2],[col],[row],[x],[y]\n``:

* client to server.

* *operation*:

    0. Blue Dot released.

    1. Blue Dot pressed.

    2. Blue Dot pressed position moved.

* *col* and *row* specify the button's position in the matrix

* *x* & *y* specify the position on the Blue Dot that was pressed, released, and/or moved:

    - Positions are values between -1 and +1, with 0 being the centre and 1 being the radius of the Blue Dot.

    - *x* is the horizontal position where +1 is far right.

    - *y* is the vertical position where +1 is the top.

*\\n* represents the ASCII new-line character (ASCII character 10).

Example
-------

When the Android client connects using protocol version 1::

    3,1,Android Blue Dot app\n

The setup of the Blue Dot is sent to the client::

    4,#0000ffff,0,0,1,1,1\n

If the "first" button at position [0,0] is pressed at the top, the following message will be sent::

    1,0,0,0.0,1.0\n

While the button is pressed (held down), the user moves their finger to the
far right causing the following message to be sent::

    2,0,0,1.0,0.0\n

The button is then released, resulting in the following message::

    0,0,0,1.0,0.0\n

The color of the button is changed to "red" the server sends to the client::

    5,#ff0000ff,0,0,1,0,0\n

Protocol versions
-----------------

* 0 - initial version
* 1 - introduction of operation 3, 4
* 2 - Blue Dot version 2, introduction of col, row for multiple buttons and operation 5