from __future__ import division

import sys
import warnings
from time import sleep, time
from threading import Event
from inspect import getfullargspec

from .btcomm import BluetoothServer
from .threads import WrapThread
from .constants import PROTOCOL_VERSION, CHECK_PROTOCOL_TIMEOUT
from .interactions import BlueDotInteraction, BlueDotPosition, BlueDotRotation, BlueDotSwipe
from .colors import parse_color, BLUE
from .exceptions import ButtonDoesNotExist


class Dot:
    """
    The internal base class for the implementation of a "button" or "buttons".
    """
    def __init__(self, color, square, border, visible):
        self._color = color
        self._square = square
        self._border = border
        self._visible = visible

        self._is_pressed_event = Event()
        self._is_released_event = Event()
        self._is_moved_event = Event()
        self._is_swiped_event = Event()
        self._is_double_pressed_event = Event()

        self._when_pressed = None
        self._when_pressed_background = False
        self._when_double_pressed = None
        self._when_double_pressed_background = False
        self._when_released = None
        self._when_released_background = False
        self._when_moved = None
        self._when_moved_background = False
        self._when_swiped = None
        self._when_swiped_background = False
        self._when_rotated = None
        self._when_rotated_background = False
        
        self._is_pressed = False
        self._position = None
        self._double_press_time = 0.3
        self._rotation_segments = 8

    @property
    def is_pressed(self):
        """
        Returns ``True`` if the button is pressed (or held).
        """
        return self._is_pressed

    @property
    def value(self):
        """
        Returns a 1 if ``.is_pressed``, 0 if not.
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
        current or last position the button was pressed, held or
        released.

        .. note::

            If the button is released (and inactive), :attr:`position` will
            return the position where it was released, until it is pressed
            again. If the button has never been pressed :attr:`position` will
            return ``None``.
        """
        return self._position

    @property
    def when_pressed(self):
        """
        Sets or returns the function which is called when the button is pressed.

        The function should accept 0 or 1 parameters, if the function accepts 1 parameter an
        instance of :class:`BlueDotPosition` will be returned representing where the button was pressed.

        The following example will print a message to the screen when the button is pressed::

            from bluedot import BlueDot

            def dot_was_pressed():
                print("The button was pressed")

            bd = BlueDot()
            bd.when_pressed = dot_was_pressed

        This example shows how the position of where the button was pressed can be obtained::

            from bluedot import BlueDot

            def dot_was_pressed(pos):
                print("The button was pressed at pos x={} y={}".format(pos.x, pos.y))

            bd = BlueDot()
            bd.when_pressed = dot_was_pressed

        The function will be run in the same thread and block, to run in a separate 
        thread use `set_when_pressed(function, background=True)`
        """
        return self._when_pressed

    @when_pressed.setter
    def when_pressed(self, value):
        self.set_when_pressed(value)
        
    def set_when_pressed(self, callback, background=False):
        """
        Sets the function which is called when the button is pressed.
        
        :param Callable callback:
            The function to call, setting to `None` will stop the callback.

        :param bool background:
            If set to `True` the function will be run in a separate thread 
            and it will return immediately. The default is `False`.
        """
        self._when_pressed = callback
        self._when_pressed_background = background

    @property
    def when_double_pressed(self):
        """
        Sets or returns the function which is called when the button is double pressed.

        The function should accept 0 or 1 parameters, if the function accepts 1 parameter an
        instance of :class:`BlueDotPosition` will be returned representing where the button was
        pressed the second time.

        The function will be run in the same thread and block, to run in a separate 
        thread use `set_when_double_pressed(function, background=True)`

        .. note::
            The double press event is fired before the 2nd press event e.g. events would be
            appear in the order, pressed, released, double pressed, pressed.
        """
        return self._when_double_pressed

    @when_double_pressed.setter
    def when_double_pressed(self, value):
        self.set_when_double_pressed(value)

    def set_when_double_pressed(self, callback, background=False):
        """
        Sets the function which is called when the button is double pressed.
        
        :param Callable callback:
            The function to call, setting to `None` will stop the callback.

        :param bool background:
            If set to `True` the function will be run in a separate thread 
            and it will return immediately. The default is `False`.
        """
        self._when_double_pressed = callback
        self._when_double_pressed_background = background

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
        Sets or returns the function which is called when the button is released.

        The function should accept 0 or 1 parameters, if the function accepts 1 parameter an
        instance of :class:`BlueDotPosition` will be returned representing where the button was held
        when it was released.

        The function will be run in the same thread and block, to run in a separate 
        thread use `set_when_released(function, background=True)`
        """
        return self._when_released

    @when_released.setter
    def when_released(self, value):
        self.set_when_released(value)

    def set_when_released(self, callback, background=False):
        """
        Sets the function which is called when the button is released.
        
        :param Callable callback:
            The function to call, setting to `None` will stop the callback.

        :param bool background:
            If set to `True` the function will be run in a separate thread 
            and it will return immediately. The default is `False`.
        """
        self._when_released = callback
        self._when_released_background = background

    @property
    def when_moved(self):
        """
        Sets or returns the function which is called when the position the button is pressed is moved.

        The function should accept 0 or 1 parameters, if the function accepts 1 parameter an
        instance of :class:`BlueDotPosition` will be returned representing the new position of where the
        Blue Dot is held.

        The function will be run in the same thread and block, to run in a separate 
        thread use `set_when_moved(function, background=True)`
        """
        return self._when_moved

    @when_moved.setter
    def when_moved(self, value):
        self.set_when_moved(value)

    def set_when_moved(self, callback, background=False):
        """
        Sets the function which is called when the position the button is pressed is moved.

        :param Callable callback:
            The function to call, setting to `None` will stop the callback.

        :param bool background:
            If set to `True` the function will be run in a separate thread 
            and it will return immediately. The default is `False`.
        """
        self._when_moved = callback
        self._when_moved_background = background

    @property
    def when_swiped(self):
        """
        Sets or returns the function which is called when the button is swiped.

        The function should accept 0 or 1 parameters, if the function accepts 1 parameter an
        instance of :class:`BlueDotSwipe` will be returned representing the how the button was
        swiped.

        The function will be run in the same thread and block, to run in a separate 
        thread use `set_when_swiped(function, background=True)`
        """
        return self._when_swiped

    @when_swiped.setter
    def when_swiped(self, value):
        self.set_when_swiped(value)

    def set_when_swiped(self, callback, background=False):
        """
        Sets the function which is called when the position the button is swiped.

        :param Callable callback:
            The function to call, setting to `None` will stop the callback.

        :param bool background:
            If set to `True` the function will be run in a separate thread 
            and it will return immediately. The default is `False`.
        """
        self._when_swiped = callback
        self._when_swiped_background = background

    @property
    def rotation_segments(self):
        """
        Sets or returns the number of virtual segments the button is split into for rotating.
        Defaults to 8.
        """
        return self._rotation_segments

    @rotation_segments.setter
    def rotation_segments(self, value):
        self._rotation_segments = value

    @property
    def when_rotated(self):
        """
        Sets or returns the function which is called when the button is rotated (like an
        iPod clock wheel).

        The function should accept 0 or 1 parameters, if the function accepts 1 parameter an
        instance of :class:`BlueDotRotation` will be returned representing how the button was
        rotated.

        The function will be run in the same thread and block, to run in a separate 
        thread use `set_when_rotated(function, background=True)`
        """
        return self._when_rotated

    @when_rotated.setter
    def when_rotated(self, value):
        self.set_when_rotated(value)

    def set_when_rotated(self, callback, background=False):
        """
        Sets the function which is called when the position the button is rotated (like an
        iPod clock wheel).

        :param Callable callback:
            The function to call, setting to `None` will stop the callback.

        :param bool background:
            If set to `True` the function will be run in a separate thread 
            and it will return immediately. The default is `False`.
        """
        self._when_rotated = callback
        self._when_rotated_background = background

    @property
    def color(self):
        """
        Sets or returns the color of the dot. Defaults to BLUE.
        
        An instance of :class:`.colors.Color` is returned.

        Value can be set as a :class:`.colors.Color` object, a hex color value
        in the format `#rrggbb` or `#rrggbbaa`, a tuple of `(red, green, blue)`
        or `(red, green, blue, alpha)` values between `0` & `255` or a text 
        description of the color, e.g. "red". 
        
        A dictionary of available colors can be obtained from `bluedot.COLORS`.
        """
        return self._color

    @color.setter
    def color(self, value):
        self._color = parse_color(value)
        
    @property
    def square(self):
        """
        When set to `True` the 'dot' is made square. Default is `False`.
        """
        return self._square

    @square.setter
    def square(self, value):
        self._square = value

    @property
    def border(self):
        """
        When set to `True` adds a border to the dot. Default is `False`.
        """
        return self._border

    @border.setter
    def border(self, value):
        self._border = value

    @property
    def visible(self):
        """
        When set to `False` the dot will be hidden. Default is `True`.

        .. note::

            Events (press, release, moved) are still sent from the dot
            when it is not visible.
        """
        return self._visible

    @visible.setter
    def visible(self, value):
        self._visible = value

    def wait_for_press(self, timeout = None):
        """
        Waits until a Blue Dot is pressed.
        Returns ``True`` if the button was pressed.

        :param float timeout:
            Number of seconds to wait for a Blue Dot to be pressed, if ``None``
            (the default), it will wait indefinetly.
        """
        return self._is_pressed_event.wait(timeout)

    def wait_for_double_press(self, timeout = None):
        """
        Waits until a Blue Dot is double pressed.
        Returns ``True`` if the button was double pressed.

        :param float timeout:
            Number of seconds to wait for a Blue Dot to be double pressed, if ``None``
            (the default), it will wait indefinetly.
        """
        return self._is_double_pressed_event.wait(timeout)

    def wait_for_release(self, timeout = None):
        """
        Waits until a Blue Dot is released.
        Returns ``True`` if the button was released.

        :param float timeout:
            Number of seconds to wait for a Blue Dot to be released, if ``None``
            (the default), it will wait indefinetly.
        """
        return self._is_released_event.wait(timeout)

    def wait_for_move(self, timeout = None):
        """
        Waits until the position where the button is pressed is moved.
        Returns ``True`` if the position pressed on the button was moved.

        :param float timeout:
            Number of seconds to wait for the position that the button
            is pressed to move, if ``None`` (the default), it will wait indefinetly.
        """
        return self._is_moved_event.wait(timeout)

    def wait_for_swipe(self, timeout = None):
        """
        Waits until the button is swiped.
        Returns ``True`` if the button was swiped.

        :param float timeout:
            Number of seconds to wait for the button to be swiped, if ``None``
            (the default), it will wait indefinetly.
        """
        return self._is_swiped_event.wait(timeout)

    def press(self, position):
        """
        Processes any "pressed" events associated with this dot.

        :param BlueDotPosition position:
            The BlueDotPosition where the dot was pressed.
        """
        self._position = position
        self._is_pressed = True
        self._is_pressed_event.set()
        self._is_pressed_event.clear()

        self._process_callback(self.when_pressed, position, self._when_pressed_background)

    def release(self, position):
        """
        Processes any "released" events associated with this dot.

        :param BlueDotPosition position:
            The BlueDotPosition where the Dot was pressed.
        """
        self._position = position
        self._is_pressed = False
        self._is_released_event.set()
        self._is_released_event.clear()

        self._process_callback(self.when_released, position, self._when_released_background)

    def move(self, position):
        """
        Processes any "released" events associated with this dot.

        :param BlueDotPosition position:
            The BlueDotPosition where the Dot was pressed.
        """
        self._is_moved_event.set()
        self._is_moved_event.clear()

        self._process_callback(self.when_moved, position, self._when_moved_background)

    def double_press(self, position):
        """
        Processes any "double press" events associated with this dot.
        
        :param BlueDotPosition position:
            The BlueDotPosition where the Dot was pressed.
        """
        self._is_double_pressed_event.set()
        self._is_double_pressed_event.clear()

        self._process_callback(self.when_double_pressed, position, self._when_double_pressed_background)

    def swipe(self, swipe):
        """
        Processes any "swipe" events associated with this dot.
        
        :param BlueDotSwipe swipe:
            The BlueDotSwipe representing how the dot was swiped.
        """
        self._is_swiped_event.set()
        self._is_swiped_event.clear()

        self._process_callback(self.when_swiped, swipe, self._when_swiped_background)

    def rotate(self, rotation):
        """
        Processes any "rotation" events associated with this dot.
        
        :param BlueDotRotation rotation:
            The BlueDotRotation representing how the dot was rotated.
        """
        # print("rotating - when_rotated {}")
        self._process_callback(self.when_rotated, rotation, self._when_rotated_background)
        
    def _process_callback(self, callback, arg, background):
        if callback:
            args_expected = getfullargspec(callback).args
            no_args_expected = len(args_expected)
            if len(args_expected) > 0:
                # if someone names the first arg of a class function to something
                # other than self, this will fail! or if they name the first argument
                # of a non class function to self this will fail!
                if args_expected[0] == "self":
                    no_args_expected -= 1

            if no_args_expected == 0:
                call_back_t = WrapThread(target=callback)
            else:
                call_back_t = WrapThread(target=callback, args=(arg, ))
            call_back_t.start()

            # if this callback is not running in the background wait for it
            if not background:
                call_back_t.join()


class BlueDotButton(Dot):
    """
    Represents a single button on the button client applications. It keeps 
    tracks of when and where the button has been pressed and processes any 
    events.

    This class is intended for use via :class:`BlueDot` and should not be 
    instantiated "manually".

    A button can be interacted with individually via :class:`BlueDot` by 
    stating its position in the grid e.g. ::

        from bluedot import BlueDot
        bd = BlueDot()

        first_button = bd[0,0].wait_for_press

        first_button.wait_for_press()
        print("The first button was pressed")

    :param BlueDot bd:
        The BlueDot object this button belongs too.

    :param int col:
        The column position for this button in the grid.

    :param int col:
        The row position for this button in the grid.

    :param string color
        The color of the button.
        
        Can be set as a :class:`.colors.Color` object, a hex color value
        in the format `#rrggbb` or `#rrggbbaa`, a tuple of `(red, green, blue)`
        or `(red, green, blue, alpha)` values between `0` & `255` or a text 
        description of the color, e.g. "red". 
        
        A dictionary of available colors can be obtained from `bluedot.COLORS`.

    :param bool square:
        When set to `True` the button is made square.

    :param bool border:
        When set to `True` adds a border to the button.

    :param bool visible:
        When set to `False` the button will be hidden.
    """
    def __init__(self, bd, col, row, color, square, border, visible):
        self._bd = bd
        self.col = col
        self.row = row
        
        self._interaction = None
   
        # setup the "dot"
        super().__init__(color, square, border, visible)

    @property
    def color(self):
        return super(BlueDotButton, self.__class__).color.fget(self)
        
    @color.setter
    def color(self, value):
        super(BlueDotButton, self.__class__).color.fset(self, value)
        self._send_config()

    @property
    def square(self):
        return super(BlueDotButton, self.__class__).square.fget(self)

    @square.setter
    def square(self, value):
        super(BlueDotButton, self.__class__).square.fset(self, value)
        self._send_config()

    @property
    def border(self):
        return super(BlueDotButton, self.__class__).border.fget(self)

    @border.setter
    def border(self, value):
        super(BlueDotButton, self.__class__).border.fset(self, value)
        self._send_config()

    @property
    def visible(self):
        return super(BlueDotButton, self.__class__).visible.fget(self)

    @visible.setter
    def visible(self, value):
        super(BlueDotButton, self.__class__).visible.fset(self, value)
        self._send_config()

    @property
    def modified(self):
        """
        Returns `True` if the button's appearance has been modified [is 
        different] from the default.  
        """
        return not (
            self.color == self._bd.color and 
            self.visible == self._bd.visible and
            self.border == self._bd.border and
            self.square == self._bd.square
            )

    @property
    def interaction(self):
        """
        Returns an instance of :class:`BlueDotInteraction` representing the
        current or last interaction with the button.

        .. note::

            If the button is released (and inactive), :attr:`interaction`
            will return the interaction when it was released, until it is
            pressed again.  If the button has never been pressed
            :attr:`interaction` will return ``None``.
        """
        return self._interaction

    def press(self, position):
        """
        Processes any "pressed" events associated with this button.

        :param BlueDotPosition position:
            The BlueDotPosition where the dot was pressed.
        """
        super().press(position)

        # create new interaction
        self._interaction = BlueDotInteraction(position)

    def release(self, position):
        """
        Processes any "released" events associated with this button.

        :param BlueDotPosition position:
            The BlueDotPosition where the Dot was pressed.
        """
        super().release(position)

        self._interaction.released(position)

    def move(self, position):
        """
        Processes any "released" events associated with this button.

        :param BlueDotPosition position:
            The BlueDotPosition where the Dot was pressed.
        """
        super().move(position)

        self._interaction.moved(position)

    def is_double_press(self, position):
        """
        Returns True if the position passed represents a double press.

        i.e. The last interaction was the button was to release it, and
        the time to press is less than the double_press_time.

        :param BlueDotPosition position:
            The BlueDotPosition where the Dot was pressed.
        """
        double_press = False
        #was there a previous interaction
        if self._interaction:
            # was the previous interaction complete (i.e. had it been released)
            if not self._interaction.active:
                # was it less than the time threshold (0.3 seconds)
                if self._interaction.duration < self._double_press_time:
                    #was the dot pressed again in less than the threshold
                    if time() - self._interaction.released_position.time < self._double_press_time:
                        double_press = True
        
        return double_press

    def get_swipe(self):
        """
        Returns an instance of :class:`BlueDotSwipe` if the last interaction
        with the button was a swipe. Returns `None` if the button was not 
        swiped. 
        """
        swipe = BlueDotSwipe(self.interaction)
        if swipe.valid:
            return swipe

    def get_rotation(self):
        """
        Returns an instance of :class:`BlueDotRotation` if the last interaction
        with the button was a rotation. Returns `None` if the button was not 
        rotated. 
        """
        # only bother checking to see if its a rotation if `when_rotated`
        # as been set. Performance thang!
        if self.when_rotated or self._bd.when_rotated:
            rotation = BlueDotRotation(self._interaction, self._rotation_segments)
            if rotation.valid:
                return rotation

    def _build_config_msg(self):
        return "5,{},{},{},{},{},{}\n".format(
                    self.color,
                    int(self.square),
                    int(self.border),
                    int(self.visible),
                    self.col,
                    self.row
                    )

    def _send_config(self):
        if self._bd.is_connected:
            self._bd._server.send(self._build_config_msg())

class BlueDot(Dot):
    """
    Interacts with a Blue Dot client application, communicating when and where a 
    button has been pressed, released or held.

    This class starts an instance of :class:`.btcomm.BluetoothServer`
    which manages the connection with the Blue Dot client.

    This class is intended for use with a Blue Dot client application.

    The following example will print a message when the Blue Dot button is pressed::

        from bluedot import BlueDot
        bd = BlueDot()
        bd.wait_for_press()
        print("The button was pressed")

    Multiple buttons can be created, by changing the number of columns and rows. Each button can be referenced using its [col, row]::

        bd = BlueDot(cols=2, rows=2)
        bd[0,0].wait_for_press()
        print("Top left button pressed")
        bd[1,1].wait_for_press()
        print("Bottom right button pressed")

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
        when the server has started and when clients connect / disconnect.

    :param int cols:
        The number of columns in the grid of buttons. Defaults to ``1``.

    :param int rows:
        The number of rows in the grid of buttons. Defaults to ``1``.

    """
    def __init__(self,
        device = "hci0",
        port = 1,
        auto_start_server = True,
        power_up_device = False,
        print_messages = True,
        cols = 1,
        rows = 1):

        self._data_buffer = ""
        self._device = device
        self._port = port
        self._power_up_device = power_up_device
        self._print_messages = print_messages

        self._check_protocol_event = Event()
        self._is_connected_event = Event()
        self._when_client_connects = None
        self._when_client_connects_background = False
        self._when_client_disconnects = None
        self._when_client_disconnects_background = False

        # setup the main "dot"
        super().__init__(BLUE, False, False, True)

        # setup the grid
        self._buttons = {}
        self.resize(cols, rows)

        self._create_server()

        if auto_start_server:
            self.start()

    @property
    def buttons(self):
        """
        A list of :class:`BlueDotButton` objects in the "grid". 
        """
        return self._buttons.values()

    @property
    def cols(self):
        """
        Sets or returns the number of columns in the grid of buttons.
        """
        return self._cols
    
    @cols.setter
    def cols(self, value):
        self.resize(value, self._rows)

    @property
    def rows(self):
        """
        Sets or returns the number of rows in the grid of buttons.
        """
        return self._rows
    
    @rows.setter
    def rows(self, value):
        self.resize(self._cols, value)

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
    def print_messages(self):
        """
        When set to ``True`` messages relating to the status of the Bluetooth server
        will be printed.
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

    @property
    def is_connected(self):
        """
        Returns ``True`` if a Blue Dot client is connected.
        """
        return self._is_connected_event.is_set()

    @property
    def is_pressed(self):
        """
        Returns ``True`` if the button is pressed (or held).

        .. note::

            If there are multiple buttons, if any button is pressed, `True`
            will be returned.
        """
        for button in self.buttons:
            if button._is_pressed:
                return True

        return False

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

            If there are multiple buttons, the interaction will only be 
            returned for button [0,0]

        .. deprecated:: 2.0.0

        """
        return self._get_button((0,0)).interaction

    @property
    def rotation_segments(self):
        """
        Sets or returns the number of virtual segments the button is split into for rotating.
        Defaults to 8.

        .. note::
        
            If there are multiple buttons in the grid, the 'default' value
            will be returned and when set all buttons will be updated.
        """
        return super(BlueDot, self.__class__).rotation_segments.fget(self)

    @rotation_segments.setter
    def rotation_segments(self, value):
        super(BlueDot, self.__class__).rotation_segments.fset(self, value)
        for button in self.buttons:
            button.rotation_segments = value

    @property
    def double_press_time(self):
        """
        Sets or returns the time threshold in seconds for a double press. Defaults to 0.3.

        .. note::
        
            If there are multiple buttons in the grid, the 'default' value
            will be returned and when set all buttons will be updated.
        """
        return super(BlueDot, self.__class__).double_press_time.fget(self)

    @double_press_time.setter
    def double_press_time(self, value):
        super(BlueDot, self.__class__).double_press_time.fset(self, value)
        for button in self.buttons:
            button.double_press_time = value

    @property
    def color(self):
        """
        Sets or returns the color of the button. Defaults to BLUE.

        An instance of :class:`.colors.Color` is returned.

        Value can be set as a :class:`.colors.Color` object, a hex color value
        in the format `#rrggbb` or `#rrggbbaa`, a tuple of `(red, green, blue)`
        or `(red, green, blue, alpha)` values between `0` & `255` or a text 
        description of the color, e.g. "red". 
        
        A dictionary of available colors can be obtained from `bluedot.COLORS`.

        .. note::
        
            If there are multiple buttons in the grid, the 'default' value
            will be returned and when set all buttons will be updated.
        """
        return super(BlueDot, self.__class__).color.fget(self)
        
    @color.setter
    def color(self, value):
        super(BlueDot, self.__class__).color.fset(self, value)
        for button in self.buttons:
            button.color = value

    @property
    def square(self):
        """
        When set to `True` the 'dot' is made square. Default is `False`.

        .. note::
        
            If there are multiple buttons in the grid, the 'default' value
            will be returned and when set all buttons will be updated.
        """
        return super(BlueDot, self.__class__).square.fget(self)

    @square.setter
    def square(self, value):
        super(BlueDot, self.__class__).square.fset(self, value)
        for button in self.buttons:
            button.square = value

    @property
    def border(self):
        """
        When set to `True` adds a border to the dot. Default is `False`.

        .. note::
        
            If there are multiple buttons in the grid, the 'default' value
            will be returned and when set all buttons will be updated.
        """
        return super(BlueDot, self.__class__).border.fget(self)

    @border.setter
    def border(self, value):
        super(BlueDot, self.__class__).border.fset(self, value)
        for button in self.buttons:
            button.border = value

    @property
    def visible(self):
        """
        When set to `False` the dot will be hidden. Default is `True`.

        .. note::

            Events (press, release, moved) are still sent from the dot
            when it is not visible.

            If there are multiple buttons in the grid, the 'default' value
            will be returned and when set all buttons will be updated.
        """
        return super(BlueDot, self.__class__).visible.fget(self)

    @visible.setter
    def visible(self, value):
        super(BlueDot, self.__class__).visible.fset(self, value)
        for button in self.buttons:
            button.visible = value

    @property
    def when_client_connects(self):
        """
        Sets or returns the function which is called when a Blue Dot 
        application connects.

        The function will be run in the same thread and block, to run in a separate 
        thread use `set_when_client_connects(function, background=True)`
        """
        return self._when_client_connects

    @when_client_connects.setter
    def when_client_connects(self, value):
        self.set_when_client_connects(value)

    def set_when_client_connects(self, callback, background=False):
        """
        Sets the function which is called when a Blue Dot connects.
        
        :param Callable callback:
            The function to call, setting to `None` will stop the callback.

        :param bool background:
            If set to `True` the function will be run in a separate thread 
            and it will return immediately. The default is `False`.
        """
        self._when_client_connects = callback
        self._when_client_connects_background = background

    @property
    def when_client_disconnects(self):
        """
        Sets or returns the function which is called when a Blue Dot disconnects.

        The function will be run in the same thread and block, to run in a separate 
        thread use `set_when_client_disconnects(function, background=True)`
        """
        return self._when_client_disconnects

    @when_client_disconnects.setter
    def when_client_disconnects(self, value):
        self.set_when_client_disconnects(value)

    def set_when_client_disconnects(self, callback, background=False):
        """
        Sets the function which is called when a Blue Dot disconnects.
        
        :param Callable callback:
            The function to call, setting to `None` will stop the callback.

        :param bool background:
            If set to `True` the function will be run in a separate thread 
            and it will return immediately. The default is `False`.
        """
        self._when_client_disconnects = callback
        self._when_client_disconnects_background = background

    def wait_for_connection(self, timeout = None):
        """
        Waits until a Blue Dot client connects.
        Returns ``True`` if a client connects.

        :param float timeout:
            Number of seconds to wait for a wait connections, if ``None`` (the default),
            it will wait indefinetly for a connection from a Blue Dot client.
        """
        return self._is_connected_event.wait(timeout)

    def start(self):
        """
        Start the :class:`.btcomm.BluetoothServer` if it is not already 
        running. By default the server is started at initialisation.
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

    def allow_pairing(self, timeout = 60):
        """
        Allow a Bluetooth device to pair with your Raspberry Pi by putting
        the adapter into discoverable and pairable mode.

        :param int timeout:
            The time in seconds the adapter will remain pairable. If set to ``None``
            the device will be discoverable and pairable indefinetly.
        """
        self.server.adapter.allow_pairing(timeout = timeout)

    def resize(self, cols, rows):
        """
        Resizes the grid of buttons. 

        :param int cols:
            The number of columns in the grid of buttons.

        :param int rows:
            The number of rows in the grid of buttons.

        .. note::
            Existing buttons will retain their state (color, border, etc) when 
            resized. New buttons will be created with the default values set 
            by the :class:`BlueDot`.
        """
        self._cols = cols
        self._rows = rows        

        # create new buttons
        new_buttons = {}

        for c in range(cols):
            for r in range(rows):
                # if button already exist, reuse it
                if (c,r) in self._buttons.keys():
                    new_buttons[c,r] = self._buttons[c,r]
                else:   
                    new_buttons[c,r] = BlueDotButton(self, c, r, self._color, self._square, self._border, self._visible)
                
        self._buttons = new_buttons

        self._send_bluedot_config()

    def _get_button(self, key):
        try:
            return self._buttons[key]
        except KeyError:
            raise ButtonDoesNotExist("The button `{}` does not exist".format(key))

    def _client_connected(self):
        self._is_connected_event.set()
        self._print_message("Client connected {}".format(self.server.client_address))
        self._send_bluedot_config()
        if self.when_client_connects:
            self._process_callback(self.when_client_connects, None, self._when_client_connects_background)
        
        # wait for the protocol version to be checked.
        if not self._check_protocol_event.wait(CHECK_PROTOCOL_TIMEOUT):
            self._print_message("Protocol version not received from client - do you need to update the client to the latest version?")
            self._server.disconnect_client()

    def _client_disconnected(self):
        self._is_connected_event.clear()
        self._check_protocol_event.clear()
        self._print_message("Client disconnected")
        if self.when_client_disconnects:
            self._process_callback(self.when_client_disconnects, None, self._when_client_disconnects_background)

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
            # debug - print each command
            # print(command)

            operation = command.split(",")[0]
            params = command.split(",")[1:]
            
            # dot change operation?
            if operation in ["0", "1", "2"]:

                position = None
                try:
                    button, position = self._parse_interaction_msg(operation, params)
                    self._position = position
                except ValueError:
                    # warn about the occasional corrupt command
                    warnings.warn("Data received which could not be parsed.\n{}".format(command))
                except ButtonDoesNotExist:
                    # data received for a button which could not be found
                    warnings.warn("Data received for a button which does not exist.\n{}".format(command))
                else:
                    # dot released
                    if operation == "0":
                        self._process_release(button, position)
                        
                    # dot pressed
                    elif operation == "1":
                        self._process_press(button, position)
                        
                    # dot pressed position moved 
                    elif operation == "2":
                        self._process_move(button, position)
                        
            # protocol check
            elif operation == "3":
                self._check_protocol_version(params[0], params[1])

            else:
                # operation not identified...  
                warnings.warn("Data received for an unknown operation.\n{}".format(command))

    def _parse_interaction_msg(self, operation, params):
        """
        Parses an interaction (press, move, release) message and returns 
        the component parts
        """
        # parse message
        col = int(params[0])
        row = int(params[1])
        position = BlueDotPosition(col, row, params[2], params[3])
        button = self._get_button((col, row))
        
        return button, position

    def _process_press(self, button, position):
        # was the button double pressed?
        if button.is_double_press(position):
            self.double_press(position)
            button.double_press(position)
        
        # set the blue dot and button as pressed
        self.press(position)
        button.press(position)

    def _process_move(self, button, position):
        # set the blue dot as moved
        self.move(position)
        # set the button as moved
        button.move(position)
        # was it a rotation
        rotation = button.get_rotation()
        if rotation is not None:
            self.rotate(rotation)
            button.rotate(rotation)

    def _process_release(self, button, position):
        # set the blue dot as released
        self.release(position)
        # set the button as released
        button.release(position)
        
        # was it a swipe?
        swipe = button.get_swipe()
        if swipe is not None:
            self.swipe(swipe)
            button.swipe(swipe)
                    
    def _check_protocol_version(self, protocol_version, client_name):
        try:
            version_no = int(protocol_version)
        except ValueError:
            raise ValueError("protocol version number must be numeric, received {}.".format(protocol_version)) 
        self._check_protocol_event.set()
        
        if version_no != PROTOCOL_VERSION:
            msg = "Client '{}' was using protocol version {}, bluedot python library is using version {}. "
            if version_no > PROTOCOL_VERSION:
                msg += "Update the bluedot python library, using 'sudo pip3 --upgrade install bluedot'."
                msg = msg.format(client_name, protocol_version, PROTOCOL_VERSION)
            else:
                msg += "Update the {}."
                msg = msg.format(client_name, protocol_version, PROTOCOL_VERSION, client_name)
            self._server.disconnect_client()
            print(msg)
        
    # called whenever the BlueDot configuration is changed or a client connects
    def _send_bluedot_config(self):
        if self.is_connected:
            self._server.send(
                "4,{},{},{},{},{},{}\n".format(
                    self._color.str_rgba, 
                    int(self._square),
                    int(self._border),
                    int(self._visible),
                    self._cols,
                    self._rows
                    )
                )

            # send the configuration for the individual buttons
            button_config_msg = ""
            for button in self.buttons:
                if button.modified:
                    button_config_msg += button._build_config_msg()

            if button_config_msg != "":
                self._server.send(button_config_msg)

    def _print_message(self, message):
        if self.print_messages:
            print(message)

    def __getitem__(self, key):
        return self._get_button(key)
