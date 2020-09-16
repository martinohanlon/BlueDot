Change log
==========

.. currentmodule:: bluedot

Bluedot Python library
----------------------

2.0.0 - tbc
~~~~~~~~~~~~~~~~~~

 * implementation of multiple buttons in a matrix
 * refactor of significant portions of the code base
 * improvement to btcomm to manage large messages 
 * update to MockBlueDot
 * deprecated BlueDot.interaction
 * added warnings when invalid data is received
 * support for protocol version 2
 * removed support for Python 2, 3.3 & 3.4

1.3.2 - 2019-04-22
~~~~~~~~~~~~~~~~~~

 * change to how callbacks are called
 * added `set_when_pressed`, `set_when_released`, etc to allow callbacks to be called in their own threads.

1.3.1 - 2019-01-01
~~~~~~~~~~~~~~~~~~

 * minor bug fix to launch_mock_app

1.3.0 - 2018-12-30
~~~~~~~~~~~~~~~~~~

 * added ability to change the color, border, shape and visibility of the dot (:attr:`~BlueDot.color`, :attr:`~BlueDot.border`, :attr:`~BlueDot.square`, :attr:`~BlueDot.visible`)
 * added protocol version checking
 * minor threading changes in btcomm
 * updates to the Blue Dot Python app
 * rewrite of the mock app
 * support for protocol version 1
 
1.2.3 - 2018-02-22
~~~~~~~~~~~~~~~~~~

 * fix to `wait_for_press` and `wait_for_release`
 * when_client_connects and when_client_disconnects callbacks are now threaded
 * The python blue dot app can now be started with the command `bluedotapp`
 * new tests for `wait_for_(events)`

1.2.2 - 2017-12-30
~~~~~~~~~~~~~~~~~~

 * bluetooth comms tests and minor bug fix in :class:`~.btcomm.BluetoothClient`

1.2.1 - 2017-12-18
~~~~~~~~~~~~~~~~~~

 * massive code and docs tidy up by `Dave Jones`_

1.2.0 - 2017-12-10
~~~~~~~~~~~~~~~~~~

 * added when_rotated
 * threaded swipe callbacks
 * exposed new :class:`BlueDot` properties (:attr:`~BlueDot.adapter`, :attr:`~BlueDot.running`, :attr:`~BlueDot.paired_devices`)
 * fixed active bug in interaction
 * automated tests

1.1.0 - 2017-11-05
~~~~~~~~~~~~~~~~~~

 * threaded callbacks
 * python app rounded x,y performance improvements

1.0.4 - 2017-09-10
~~~~~~~~~~~~~~~~~~

 * serial port profile port fix
 * launching multiple blue dots fix

1.0.3 - 2017-07-28
~~~~~~~~~~~~~~~~~~

 * python 2 bug fix

1.0.2 - 2017-07-23
~~~~~~~~~~~~~~~~~~

 * bug fix

1.0.1 - 2017-06-19
~~~~~~~~~~~~~~~~~~

 * bug fixes

1.0.0 - 2017-06-04
~~~~~~~~~~~~~~~~~~

 * production release!
 * added double click
 * doc updates
 * minor changes

0.4.0 - 2017-05-05
~~~~~~~~~~~~~~~~~~

 * added swipes and interactions
 * doc updates
 * bug fix in :attr:`BlueDot.when_moved`

0.3.0 - 2017-05-01
~~~~~~~~~~~~~~~~~~

 * Python Blue Dot app
 * minor bug fix in :class:`~.btcomm.BluetoothClient`

0.2.1 - 2017-04-23
~~~~~~~~~~~~~~~~~~

 * bug fix in :class:`MockBlueDot`
 * doc fixes

0.2.0 - 2017-04-23
~~~~~~~~~~~~~~~~~~

 * added :attr:`~BlueDot.when_client_connects`, :attr:`~BlueDot.when_client_disconnects`
 * added :meth:`~BlueDot.allow_pairing` functions
 * refactored Bluetooth comms
 * added :class:`~.btcomm.BluetoothAdapter`

0.1.2 - 2017-04-14
~~~~~~~~~~~~~~~~~~

 * mock blue dot improvements
 * doc fixes

0.1.1 - 2017-04-08
~~~~~~~~~~~~~~~~~~

 * clamped distance in :class:`BlueDotPosition`

0.1.0 - 2017-04-07
~~~~~~~~~~~~~~~~~~

 * Check Bluetooth adapter is powered
 * Handle client connection timeouts
 * Docs & image updates

0.0.6 - 2017-04-05
~~~~~~~~~~~~~~~~~~

 * Added :class:`MockBlueDot` for testing and debugging
 * more docs

0.0.4 - 2017-03-31
~~~~~~~~~~~~~~~~~~

Updates after alpha feedback

 * Python 2 compatibility
 * ``.dot_position`` to ``.position``
 * ``.values`` added
 * clamped ``x``, ``y`` to 1
 * loads of doc updates

0.0.2 - 2017-03-29
~~~~~~~~~~~~~~~~~~

Alpha - initial testing

Android app
-----------

7 (2.0) - tbc
~~~~~~~~~~~~~~~~~~~~~~~~

 * implementation of multiple buttons in a matrix
 * support for protocol version 2

6 (1.3.1) - 2019-12-30
~~~~~~~~~~~~~~~~~~~~~~~~

 * Minor bug fix

5 (1.3) - 2019-12-29
~~~~~~~~~~~~~~~~~~~~~~~~

 * Added settings menu so a specific bluetooth port can be selected
 * Using specific bluetooth ports, multiple apps can now connect to a single BT devices
 * Minor bugs fixes

4 (1.2) - 2018-12-30
~~~~~~~~~~~~~~~~~~~~~~~~

 * Rewrite of the Button view
 * Rewrite of the Bluetooth comms layer
 * Support for colours, square and border
 * Landscape (and portrait) views
 * added protocol version checking
 * support for protocol version 1

3 (1.1.1) - 2018-09-21
~~~~~~~~~~~~~~~~~~~~~~~~

 * Android SDK version uplift (due to google play store minimum requirements change)

2 (1.1) - 2017-11-05
~~~~~~~~~~~~~~~~~~~~~~~~

 * better responsive layout
 * fixed issues with small screen devices
 * rounded x,y values increasing performance
 * new help icon
 * link to https://bluedot.readthedocs.io not http

1 (0.0.2) - 2017-04-05
~~~~~~~~~~~~~~~~~~~~~~~~

 * icon transparency
 * connection monitor
 * added info icon to https://bluedot.readthedocs.io

0 (0.0.1) - 2017-03-29
~~~~~~~~~~~~~~~~~~~~~~~~

 * alpha - initial testing

.. _Dave Jones: https://github.com/waveform80