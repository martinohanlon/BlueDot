from __future__ import division

import sys
from time import sleep, time
from threading import Event
from math import atan2, degrees, hypot

try:
    from inspect import getfullargspec
except ImportError:
    from inspect import getargspec as getfullargspec

from .btcomm import BluetoothServer
from .threads import WrapThread


class BlueDotPosition():
    """
    Represents a position of where the blue dot is pressed, released or held.

    :param float x:
        The x position of the Blue Dot, 0 being centre, -1 being far left
        and 1 being far right.

    :param float y:
        The y position of the Blue Dot, 0 being centre, -1 being at the
        bottom and 1 being at the top.
    """
    def __init__(self, x, y):
        self._time = time()
        self._x = self._clamped(float(x))
        self._y = self._clamped(float(y))
        self._angle = None
        self._distance = None

    def _clamped(self, v):
        return max(-1, min(1, v))

    @property
    def x(self):
        """
        The x position of the Blue Dot, 0 being centre, -1 being far
        left and 1 being far right.
        """
        return self._x

    @property
    def y(self):
        """
        The y position of the Blue Dot, 0 being centre, -1 being at
        the bottom and 1 being at the top.
        """
        return self._y

    @property
    def angle(self):
        """
        The angle from centre of where the Blue Dot is pressed, held or released.
        0 degress is up, 0..180 degrees clockwise, -180..0 degrees anti-clockwise.
        """
        if self._angle is None:
            self._angle = degrees(atan2(self.x, self.y))
        return self._angle

    @property
    def distance(self):
        """
        The distance from centre of where the Blue Dot is pressed, held or released.
        The radius of the Blue Dot is 1.
        """
        if self._distance is None:
            self._distance = self._clamped(hypot(self.x, self.y))
        return self._distance

    @property
    def middle(self):
        """
        Returns ``True`` if the Blue Dot is pressed, held or released in the middle.
        """
        return self.distance <= 0.5

    @property
    def top(self):
        """
        Returns ``True`` if the Blue Dot is pressed, held or released at the top.
        """
        return self.distance > 0.5 and (-45 < self.angle <= 45)

    @property
    def right(self):
        """
        Returns ``True`` if the Blue Dot is pressed, held or released on the right.
        """
        return self.distance > 0.5 and (45 < self.angle <= 135)

    @property
    def bottom(self):
        """
        Returns ``True`` if the Blue Dot is pressed, held or released at the bottom.
        """
        return self.distance > 0.5 and (self.angle > 135 or self.angle <= -135)

    @property
    def left(self):
        """
        Returns ``True`` if the Blue Dot is pressed, held or released on the left.
        """
        return self.distance > 0.5 and (-135 < self.angle <= -45)

    @property
    def time(self):
        """
        The time the blue dot was at this position.

        .. note::

            This is the time the message was received from the Blue Dot app,
            not the time it was sent.
        """
        return self._time


class BlueDotInteraction():
    """
    Represents an interaction with the Blue Dot, from when it was pressed to
    when it was released.

    A :class:`BlueDotInteraction` can be active or inactive, i.e. it is active
    because the Blue Dot has not been released, or inactive because the Blue
    Dot was released and the interaction finished.

    :param BlueDotPosition pressed_position:
        The BlueDotPosition when the Blue Dot was pressed.
    """
    def __init__(self, pressed_position):
        self._active = True
        self._positions = []
        self._positions.append(pressed_position)

    @property
    def active(self):
        """
        Returns ``True`` if the interaction is still active, i.e. the Blue Dot
        hasnt been released.
        """
        return self._active

    @property
    def positions(self):
        """
        A sequence of :class:`BlueDotPosition` instances for all the positions
        which make up this interaction.

        The first position is where the Blue Dot was pressed, the last is where
        the Blue Dot was released, all position in between are where the position
        Blue Dot changed (i.e. moved) when it was held down.
        """
        return self._positions

    @property
    def pressed_position(self):
        """
        Returns the position when the Blue Dot was pressed i.e. where the
        interaction started.
        """
        return self._positions[0]

    @property
    def released_position(self):
        """
        Returns the position when the Blue Dot was released i.e. where the
        interaction ended.

        If the interaction is still active it returns ``None``.
        """
        return self._positions[-1] if not self.active else None

    @property
    def current_position(self):
        """
        Returns the current position for the interaction.

        If the interaction is inactive, it will return the position when the
        Blue Dot was released.
        """
        return self._positions[-1]

    @property
    def previous_position(self):
        """
        Returns the previous position for the interaction.

        If the interaction contains only 1 position, None will be returned.
        """
        return self._positions[-2] if len(self._positions) > 1 else None

    @property
    def duration(self):
        """
        Returns the duration in seconds of the interaction, i.e. the amount time
        between when the Blue Dot was pressed and now or when it was released.
        """
        if self.active:
            return time() - self.pressed_position.time
        else:
            return self.released_position.time - self.pressed_position.time

    @property
    def distance(self):
        """
        Returns the total distance of the Blue Dot interaction
        """
        dist = 0
        for i in range(1, len(self._positions)):
            p1 = self._positions[i-1]
            p2 = self._positions[i]
            dist += hypot(p2.x - p1.x, p2.y - p1.y)

        return dist

    def moved(self, moved_position):
        """
        Adds an additional position to the interaction, called when the position
        the Blue Dot is pressed moves.
        """
        if self._active:
            self._positions.append(moved_position)

    def released(self, released_position):
        """
        Called when the Blue Dot is released and completes a Blue Dot interaction

        :param BlueDotPosition released_position:
            The BlueDotPosition when the Blue Dot was released.
        """
        self._active = False
        self._positions.append(released_position)


class BlueDotSwipe():
    """
    Represents a Blue Dot swipe interaction.

    A :class:`BlueDotSwipe` can be valid or invalid based on whether the Blue Dot
    interaction was a swipe or not.

    :param BlueDotInteraction interaction:
        The BlueDotInteraction object to be used to determine whether the interaction
        was a swipe.
    """
    def __init__(self, interaction):
        self._interaction = interaction
        self._speed_threshold = 2
        self._angle = None
        self._distance = None
        self._valid = self._is_valid_swipe()

    def _is_valid_swipe(self):
        #the validity of a swipe is based on the speed of the interaction,
        # so a short fast swipe is valid as well as a long slow swipe
        #self._speed = self.distance / self.interaction.duration
        self._speed = self.distance / self.interaction.duration
        if not self.interaction.active and self._speed > self._speed_threshold:
            return True
        else:
            return False

    @property
    def interaction(self):
        """
        The :class:`BlueDotInteraction` object relating to this swipe.
        """
        return self._interaction

    @property
    def valid(self):
        """
        Returns ``True`` if the Blue Dot interaction is a swipe.
        """
        return self._valid

    @property
    def distance(self):
        """
        Returns the distance of the swipe (i.e. the distance between the pressed
        and released positions)
        """
        #should this be the total lenght of the swipe. All the points? It might be slow to calculate
        if self._distance == None:
            self._distance = hypot(
                self.interaction.released_position.x - self.interaction.pressed_position.x,
                self.interaction.released_position.y - self.interaction.pressed_position.y)

        return self._distance

    @property
    def angle(self):
        """
        Returns the angle of the swipe (i.e. the angle between the pressed
        and released positions)
        """
        if self._angle == None:
            self._angle = degrees(atan2(
                self.interaction.released_position.x - self.interaction.pressed_position.x,
                self.interaction.released_position.y - self.interaction.pressed_position.y))

        return self._angle

    @property
    def speed(self):
        """
        Returns the speed of the swipe in Blue Dot radius / second.
        """
        return self._speed

    @property
    def up(self):
        """
        Returns ``True`` if the Blue Dot was swiped up.
        """
        return self.valid and (-45 < self.angle <= 45)

    @property
    def down(self):
        """
        Returns ``True`` if the Blue Dot was swiped down.
        """
        return self.valid and (self.angle > 135 or self.angle <= -135)

    @property
    def left(self):
        """
        Returns ``True`` if the Blue Dot was swiped left.
        """
        return self.valid and (-135 < self.angle <= -45)

    @property
    def right(self):
        """
        Returns ``True`` if the Blue Dot was swiped right.
        """
        return self.valid and (45 < self.angle <= 135)


class BlueDotRotation():
    def __init__(self, interaction, no_of_segments):
        """
        Represents a Blue Dot rotation.

        A :class:`BlueDotRotation` can be valid or invalid based on whether the Blue Dot
        interaction was a rotation or not.

        :param BlueDotInteraction interaction:
            The object to be used to determine whether the interaction
            was a rotation.
        """
        self._value = 0
        self._clockwise = False
        self._anti_clockwise = False
        self._previous_segment = 0
        self._current_segment = 0

        prev_pos = interaction.previous_position
        pos = interaction.current_position

        # was there a previous position (i.e. the interaction has more than 2 positions)
        if prev_pos != None:

            # were both positions in the 'outer circle'
            if prev_pos.distance > 0.5 and pos.distance > 0.5:

                # what segments are the positions in
                deg_per_seg = (360 / no_of_segments)
                self._previous_segment = int((prev_pos.angle + 180) / deg_per_seg) + 1
                self._current_segment = int((pos.angle + 180) / deg_per_seg) + 1

                # were the positions in different segments
                if self._previous_segment != self._current_segment:
                    # calculate the rotation
                    diff = self._previous_segment - self._current_segment
                    if diff != 0:
                        if diff == -1:
                            self._value = 1
                        elif diff == 1:
                            self._value = -1
                        elif diff == (no_of_segments - 1):
                            self._value = 1
                        elif diff == (1 - no_of_segments):
                            self._value = -1

    @property
    def valid(self):
        """
        Returns ``True`` if the Blue Dot was rotated.
        """
        return self._value != 0

    @property
    def value(self):
        """
        Returns 0 if the Blue Dot wasn't rotated, -1 if rotated anti-clockwise and 1 if rotated clockwise.
        """
        return self._value

    @property
    def anti_clockwise(self):
        """
        Returns ``True`` if the Blue Dot was rotated anti-clockwise.
        """
        return self._value == -1

    @property
    def clockwise(self):
        """
        Returns ``True`` if the Blue Dot was rotated clockwise.
        """
        return self._value == 1


class BlueDot():
    """
    Interacts with a Blue Dot client application, communicating when and where it
    has been pressed, released or held.

    This class starts an instance of :class:`.btcomm.BluetoothServer`
    which manages the connection with the Blue Dot client.

    This class is intended for use with the Blue Dot client application.

    The following example will print a message when the Blue Dot is pressed::

        from bluedot import BlueDot
        bd = BlueDot()
        bd.wait_for_press()
        print("The blue dot was pressed")

    :param str device:
        The Bluetooth device the server should use, the default is "hci0", if
        your device only has 1 Bluetooth adapter this shouldn't need to be changed.

    :param int port:
        The Bluetooth port the server should use, the default is 1, and under
        normal use this should never need to change.

    :param bool auto_start_server:
        If ``True`` (the default), the Bluetooth server will be automatically
        started on initialisation; if ``False``, the method :meth:`start` will
        need to be called before connections will be accepted.

    :param bool power_up_device:
        If ``True``, the Bluetooth device will be powered up (if required) when the
        server starts. The default is ``False``.

        Depending on how Bluetooth has been powered down, you may need to use :command:`rfkill`
        to unblock Bluetooth to give permission to bluez to power on Bluetooth::

            sudo rfkill unblock bluetooth

    :param bool print_messages:
        If ``True`` (the default), server status messages will be printed stating
        when the server has started and when clients connect / disconect.

    """
    def __init__(self,
        device = "hci0",
        port = 1,
        auto_start_server = True,
        power_up_device = False,
        print_messages = True):

        self._data_buffer = ""
        self._device = device
        self._port = port
        self._power_up_device = power_up_device
        self._print_messages = print_messages

        self._is_pressed = False

        self._is_connected_event = Event()
        self._is_pressed_event = Event()
        self._is_released_event = Event()
        self._is_moved_event = Event()
        self._is_swiped_event = Event()
        self._is_double_pressed_event = Event()

        self._waiting_for_press = Event()

        self._when_pressed = None
        self._when_double_pressed = None
        self._when_released = None
        self._when_moved = None
        self._when_swiped = None
        self._when_rotated = None
        self._when_client_connects = None
        self._when_client_disconnects = None

        self._position = None
        self._interaction = None
        self._double_press_time = 0.3
        self._rotation_segments = 8

        self._create_server()

        if auto_start_server:
            self.start()

    @property
    def device(self):
        """
        The Bluetooth device the server is using. This defaults to "hci0".
        """
        return self._device

    @property
    def port(self):
        """
        The port the server is using. This defaults to 1.
            """
        return self._port

    @property
    def server(self):
        """
        The :class:`.btcomm.BluetoothServer` instance that is being used to communicate
        with clients.
        """
        return self._server

    @property
    def adapter(self):
        """
        The :class:`.btcomm.BluetoothAdapter` instance that is being used.
        """
        return self._server.adapter

    @property
    def paired_devices(self):
        """
        Returns a sequence of devices paired with this adapter
        :code:`[(mac_address, name), (mac_address, name), ...]`::

            bd = BlueDot()
            devices = bd.paired_devices
            for d in devices:
                device_address = d[0]
                device_name = d[1]
        """
        return self._server.adapter.paired_devices

    @property
    def is_connected(self):
        """
        Returns ``True`` if a Blue Dot client is connected.
        """
        return self._is_connected_event.is_set()

    @property
    def is_pressed(self):
        """
        Returns ``True`` if the Blue Dot is pressed (or held).
        """
        return self._is_pressed

    @property
    def value(self):
        """
        Returns a 1 if the Blue Dot is pressed, 0 if released.
        """
        return 1 if self.is_pressed else 0

    @property
    def values(self):
        """
        Returns an infinite generator constantly yielding the current value.
        """
        while True:
            yield self.value

    @property
    def position(self):
        """
        Returns an instance of :class:`BlueDotPosition` representing the
        current or last position the Blue Dot was pressed, held or
        released.

        .. note::

            If the Blue Dot is released (and inactive), :attr:`position` will
            return the position where it was released, until it is pressed
            again. If the Blue Dot has never been pressed :attr:`position` will
            return ``None``.
        """
        return self._position

    @property
    def interaction(self):
        """
        Returns an instance of :class:`BlueDotInteraction` representing the
        current or last interaction with the Blue Dot.

        .. note::

            If the Blue Dot is released (and inactive), :attr:`interaction`
            will return the interaction when it was released, until it is
            pressed again.  If the Blue Dot has never been pressed
            :attr:`interaction` will return ``None``.
        """
        return self._interaction

    @property
    def when_pressed(self):
        """
        Sets or returns the function which is called when the Blue Dot is pressed.

        The function should accept 0 or 1 parameters, if the function accepts 1 parameter an
        instance of :class:`BlueDotPosition` will be returned representing where the Blue Dot was pressed.

        The following example will print a message to the screen when the button is pressed::

            from bluedot import BlueDot

            def dot_was_pressed():
                print("The Blue Dot was pressed")

            bd = BlueDot()
            bd.when_pressed = dot_was_pressed

        This example shows how the position of where the dot was pressed can be obtained::

            from bluedot import BlueDot

            def dot_was_pressed(pos):
                print("The Blue Dot was pressed at pos x={} y={}".format(pos.x, pos.y))

            bd = BlueDot()
            bd.when_pressed = dot_was_pressed

        """
        return self._when_pressed

    @when_pressed.setter
    def when_pressed(self, value):
        self._when_pressed = value

    @property
    def when_double_pressed(self):
        """
        Sets or returns the function which is called when the Blue Dot is double pressed.

        The function should accept 0 or 1 parameters, if the function accepts 1 parameter an
        instance of :class:`BlueDotPosition` will be returned representing where the Blue Dot was
        pressed the second time.

        Note - the double press event is fired before the 2nd press event e.g. events would be
        appear in the order, pressed, released, double pressed, pressed.
        """
        return self._when_double_pressed

    @when_double_pressed.setter
    def when_double_pressed(self, value):
        self._when_double_pressed = value

    @property
    def double_press_time(self):
        """
        Sets or returns the time threshold in seconds for a double press. Defaults to 0.3.
        """
        return self._double_press_time

    @double_press_time.setter
    def double_press_time(self, value):
        self._double_press_time = value

    @property
    def when_released(self):
        """
        Sets or returns the function which is called when the Blue Dot is released.

        The function should accept 0 or 1 parameters, if the function accepts 1 parameter an
        instance of :class:`BlueDotPosition` will be returned representing where the Blue Dot was held
        when it was released.
        """
        return self._when_released

    @when_released.setter
    def when_released(self, value):
        self._when_released = value

    @property
    def when_moved(self):
        """
        Sets or returns the function which is called when the position the Blue Dot is pressed is moved.

        The function should accept 0 or 1 parameters, if the function accepts 1 parameter an
        instance of :class:`BlueDotPosition` will be returned representing the new position of where the
        Blue Dot is held.
        """
        return self._when_moved

    @when_moved.setter
    def when_moved(self, value):
        self._when_moved = value

    @property
    def when_swiped(self):
        """
        Sets or returns the function which is called when the Blue Dot is swiped.

        The function should accept 0 or 1 parameters, if the function accepts 1 parameter an
        instance of :class:`BlueDotSwipe` will be returned representing the how the Blue Dot was
        swiped.
        """
        return self._when_swiped

    @when_swiped.setter
    def when_swiped(self, value):
        self._when_swiped = value

    @property
    def rotation_segments(self):
        """
        Sets or returns the number of virtual segments the Blue Dot is split into for  rotating.
        Defaults to 8.
        """
        return self._rotation_segments

    @rotation_segments.setter
    def rotation_segments(self, value):
        self._rotation_segments = value

    @property
    def when_rotated(self):
        """
        Sets or returns the function which is called when the Blue Dot is rotated (like an
        iPod clock wheel).

        The function should accept 0 or 1 parameters, if the function accepts 1 parameter an
        instance of :class:`BlueDotRotation` will be returned representing how the Blue Dot was
        rotated.
        """
        return self._when_rotated

    @when_rotated.setter
    def when_rotated(self, value):
        self._when_rotated = value

    @property
    def when_client_connects(self):
        """
        Sets or returns the function which is called when a Blue Dot connects.
        """
        return self._when_client_connects

    @when_client_connects.setter
    def when_client_connects(self, value):
        self._when_client_connects = value

    @property
    def when_client_disconnects(self):
        """
        Sets or returns the function which is called when a Blue Dot disconnects.
        """
        return self._when_client_disconnects

    @when_client_disconnects.setter
    def when_client_disconnects(self, value):
        self._when_client_disconnects = value

    @property
    def print_messages(self):
        """
        When set to ``True`` results in messages relating to the status of the Bluetooth server
        to be printed.
        """
        return self._print_messages

    @print_messages.setter
    def print_messages(self, value):
        self._print_messages = value

    @property
    def running(self):
        """
        Returns a ``True`` if the server is running.
        """
        return self._server.running

    def start(self):
        """
        Start the :class:`.btcomm.BluetoothServer` if it is not already running. By default the server is started at
        initialisation.
        """
        self._server.start()
        self._print_message("Server started {}".format(self.server.server_address))
        self._print_message("Waiting for connection")

    def _create_server(self):
        self._server = BluetoothServer(
                self._data_received,
                when_client_connects = self._client_connected,
                when_client_disconnects = self._client_disconnected,
                device = self.device,
                port = self.port,
                power_up_device = self._power_up_device,
                auto_start = False)

    def stop(self):
        """
        Stop the Bluetooth server.
        """
        self._server.stop()

    def wait_for_connection(self, timeout = None):
        """
        Waits until a Blue Dot client connects.
        Returns ``True`` if a client connects.

        :param float timeout:
            Number of seconds to wait for a wait connections, if ``None`` (the default),
            it will wait indefinetly for a connection from a Blue Dot client.
        """
        return self._is_connected_event.wait(timeout)

    def wait_for_press(self, timeout = None):
        """
        Waits until a Blue Dot is pressed.
        Returns ``True`` if the Blue Dot was pressed.

        :param float timeout:
            Number of seconds to wait for a Blue Dot to be pressed, if ``None``
            (the default), it will wait indefinetly.
        """
        return self._is_pressed_event.wait(timeout)

    def wait_for_double_press(self, timeout = None):
        """
        Waits until a Blue Dot is double pressed.
        Returns ``True`` if the Blue Dot was double pressed.

        :param float timeout:
            Number of seconds to wait for a Blue Dot to be double pressed, if ``None``
            (the default), it will wait indefinetly.
        """
        return self._is_double_pressed_event.wait(timeout)

    def wait_for_release(self, timeout = None):
        """
        Waits until a Blue Dot is released.
        Returns ``True`` if the Blue Dot was released.

        :param float timeout:
            Number of seconds to wait for a Blue Dot to be released, if ``None``
            (the default), it will wait indefinetly.
        """
        return self._is_released_event.wait(timeout)

    def wait_for_move(self, timeout = None):
        """
        Waits until the position where the Blue Dot is pressed is moved.
        Returns ``True`` if the position pressed on the Blue Dot was moved.

        :param float timeout:
            Number of seconds to wait for the position that the Blue Dot
            is pressed to move, if ``None`` (the default), it will wait indefinetly.
        """
        return self._is_moved_event.wait(timeout)

    def wait_for_swipe(self, timeout = None):
        """
        Waits until the Blue Dot is swiped.
        Returns ``True`` if the Blue Dot was swiped.

        :param float timeout:
            Number of seconds to wait for the Blue Dot to be swiped, if ``None``
            (the default), it will wait indefinetly.
        """
        return self._is_swiped_event.wait(timeout)

    def allow_pairing(self, timeout = 60):
        """
        Allow a Bluetooth device to pair with your Raspberry Pi by Putting the adapter
        into discoverable and pairable mode.

        :param int timeout:
            The time in seconds the adapter will remain pairable. If set to ``None``
            the device will be discoverable and pairable indefinetly.
        """
        self.server.adapter.allow_pairing(timeout = timeout)

    def _client_connected(self):
        self._is_connected_event.set()
        self._print_message("Client connected {}".format(self.server.client_address))
        if self.when_client_connects:
            self._process_callback(self.when_client_connects, None)

    def _client_disconnected(self):
        self._is_connected_event.clear()
        self._print_message("Client disconnected")
        if self.when_client_disconnects:
            self._process_callback(self.when_client_disconnects, None)

    def _data_received(self, data):
        #add the data received to the buffer
        self._data_buffer += data

        #get any full commands ended by \n
        last_command = self._data_buffer.rfind("\n")
        if last_command != -1:
            commands = self._data_buffer[:last_command].split("\n")
            #remove the processed commands from the buffer
            self._data_buffer = self._data_buffer[last_command + 1:]
            self._process_commands(commands)

    def _process_commands(self, commands):
        for command in commands:
            try:
                operation, x, y = command.split(",")
                position = BlueDotPosition(x, y)
            except ValueError:
                # ignore the occasional corrupt command; XXX warn here?
                pass
            else:
                #update the current position
                self._position = position

                #dot released
                if operation == "0":
                    self._released(position)

                #dot pressed
                elif operation == "1":
                    self._pressed(position)

                #dot pressed position moved
                elif operation == "2":
                    self._moved(position)

    def _pressed(self, position):
        self._is_pressed = True
        self._is_pressed_event.set()
        self._is_pressed_event.clear()

        self._double_pressed(position)

        #create new interaction
        self._interaction = BlueDotInteraction(position)

        self._process_callback(self.when_pressed, position)

    def _double_pressed(self, position):
        #was there a previous interaction
        if self._interaction:
            #was it less than the time threshold (0.3 seconds)
            if self._interaction.duration < self._double_press_time:
                #was the dot pressed again in less than the threshold
                if time() - self._interaction.released_position.time < self._double_press_time:
                    self._is_double_pressed_event.set()
                    self._is_double_pressed_event.clear()

                    self._process_callback(self.when_double_pressed, position)

    def _released(self, position):
        self._is_pressed = False
        self._is_released_event.set()
        self._is_released_event.clear()

        self._interaction.released(position)

        self._process_callback(self.when_released, position)

        self._process_swipe()

    def _moved(self, position):
        self._is_moved_event.set()
        self._is_moved_event.clear()

        self._interaction.moved(position)

        self._process_callback(self.when_moved, position)

        if self.when_rotated:
            self._process_rotation()

    def _process_callback(self, callback, arg):
        if callback:
            if len(getfullargspec(callback).args) == 0:
                call_back_t = WrapThread(target=callback)
            else:
                call_back_t = WrapThread(target=callback, args=(arg, ))
            call_back_t.start()

    def _process_swipe(self):
        #was the Blue Dot swiped?
        swipe = BlueDotSwipe(self._interaction)
        if swipe.valid:
            self._is_swiped_event.set()
            self._is_swiped_event.clear()
            if self.when_swiped:
                self._process_callback(self.when_swiped, swipe)

    def _process_rotation(self):
        rotation = BlueDotRotation(self._interaction, self._rotation_segments)
        if rotation.valid:
            self._process_callback(self.when_rotated, rotation)

    def _print_message(self, message):
        if self.print_messages:
            print(message)
