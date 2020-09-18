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

    [operation],[params],[*]\n

Messages are sent as utf-8 encoded strings.

*\\n* represents the new-line character.

The following operations are used to communicate between client and server.

table

Messages are constructed using the following parameters.


Messages are sent when:

1. A client connects
3. When the setup (or appearance) of a button changes
2. A button is released, pressed or moved

.. image:: images/protocol_state.png
   :alt: Diagram showing the protocol states

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

Versions
--------

* 0 - initial version
* 1 - introduction of operation 3, 4
* 2 - Blue Dot version 2, introduction of col, row for multiple buttons and operation 5