import atexit
from time import sleep
from threading import Event
from math import atan2, degrees, hypot
from inspect import getargspec

from .btcomm import BluetoothServer

class BlueDotPosition():
    """
    Represents a position of where the blue for is pressed, released or held.

    :param float x:
        The x position of the Blue Dot, 0 being centre, -1 being far left and 1 
        being far right. 

    :param float y:
        The y position of the Blue Dot, 0 being centre, -1 being at the bottom 
        and 1 being at the top. 
    """
    def __init__(self, x, y):
        self._x = self._clamped(float(x))
        self._y = self._clamped(float(y))
        self._angle = None
        self._distance = None
        
    def _clamped(self, v):                                                                 
        return max(-1, min(1, v))
        
    @property
    def x(self):
        """
        The x position of the Blue Dot, 0 being centre, -1 being far left and 1 
        being far right. 
        """
        return self._x

    @property
    def y(self):
        """
        The y position of the Blue Dot, 0 being centre, -1 being at the bottom 
        and 1 being at the top. 
        """
        return self._y

    @property
    def angle(self):
        """
        The angle from centre of where the Blue Dot is pressed, held or released.
        0 degress is up, 0 > 180 degrees clockwise, 0 > -180 degrees anti-clockwise.   
        """
        if self._angle == None:
            self._angle = degrees(atan2(self.x, self.y))
        return self._angle

    @property
    def distance(self):
        """
        The distance from centre of where the Blue Dot is pressed, held or released.
        The radius of the Blue Dot is 1.
        """
        if self._distance == None:
            self._distance = self._clamped(hypot(self.x, self.y))
        return self._distance

    @property
    def middle(self):
        """
        Returns ``True`` if the BlueDot is pressed, held or released in the middle.
        """
        return True if self.distance <= 0.5 else False

    @property
    def top(self):
        """
        Returns ``True`` if the BlueDot is pressed, held or released at the top.
        """
        return True if self.distance > 0.5 and self.angle > -45 and self.angle <= 45 else False
    
    @property
    def right(self):
        """
        Returns ``True`` if the BlueDot is pressed, held or released on the right.
        """
        return True if self.distance > 0.5 and self.angle > 45 and self.angle <= 135 else False

    @property
    def bottom(self):
        """
        Returns ``True`` if the BlueDot is pressed, held or released at the bottom.
        """        
        return True if self.distance > 0.5 and (self.angle > 135 or self.angle <= -135) else False

    @property
    def left(self):
        """
        Returns ``True`` if the BlueDot is pressed, held or released on the left.
        """        
        return True if self.distance > 0.5 and self.angle > -135 and self.angle <= -45 else False

class BlueDot():
    """
    Interacts with a Blue Dot client application, communicating when and where it
    has been pressed, released or held.   

    This class starts an instance of a bluetooth server (btcomm.BluetoothServer) 
    which manages the connection with the Blue Dot client.

    This class is intended for use with the Blue Dot client application.

    The following example will print a message when the Blue Dot is pressed::
    
        from bluedot import BlueDot
        bd = BlueDot()
        bd.wait_for_press()
        print("The blue dot was pressed")

    :param string device:
        The bluetooth device the server should use, the default is ``hci0``, if
        your device only has 1 bluetooth adapter this shouldn't need to be changed.

    :param int port:
        The bluetooth port the server should use, the default is ``1``, and under 
        normal use this should never need to change.

    :param bool auto_start_server:
        If ``True`` (the default), the bluetooth server will be automatically started
        on initialisation, if ``False``, the method ``start`` will need to use called
        before connections will be accepted.
    
    :param bool power_up_device:
        If ``True``, the bluetooth device will be powered up (if required) when the 
        server starts. The default is ``False``. 
        
        Depending on how bluetooth has been powered down, you may need to use rfkill 
        to unblock bluetooth to give permission to bluez to power on bluetooth::

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
        self._print_messages = print_messages

        self._is_connected_event = Event()
        self._is_pressed_event = Event()
        self._is_released_event = Event()
        self._is_moved_event = Event()
        self._when_pressed = None
        self._when_released = None
        self._when_moved = None
        self._when_client_connects = None
        self._when_client_disconnects = None

        self._position = None

        self._create_server()

        if auto_start_server:
            self.start()

    @property
    def device(self):
        """
        The bluetooth device the server is using. This defaults to hci0.
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
        The BluetoothServer instance that is being used to communicate
        with clients.
        """
        return self._server

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
        return self._is_pressed_event.is_set()

    @property
    def value(self):
        """
        Returns a 1 if the Blue Dot is pressed, 0 if released.
        """
        return 1 if self.is_pressed else 0
        
    @property
    def values(self):
        """
        Returns an infinite generator constantly yielding the current value
        """
        while True:
            yield self.value

    @property
    def position(self):
        """
        Returns an instance of BlueDotPosition representing the last 
        position the Blue Dot was pressed or released. 
        
        Note - if the Blue Dot is released (and inactive), the position 
        will continue to hold the position when it was released, until
        it is pressed again.
        """
        return self._position

    @property
    def when_pressed(self):
        """
        Returns the function which is called when the Blue Dot is pressed. 
        """
        return self._when_pressed

    @when_pressed.setter
    def when_pressed(self, value):
        """
        When set to a function it will cause the function to be run when the Blue Dot is pressed.
        
        The function should accept 0 or 1 parameters, if the function accepts 1 parameter an 
        instance of BlueDotPosition will be returned representing where the Blue Dot was pressed.
        
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
        self._when_pressed = value

    @property 
    def when_released(self):
        """
        Returns the function which is called when the Blue Dot is released. 
        """
        return self._when_released

    @when_released.setter
    def when_released(self, value):
        """
        When set to a function it will cause the function to be run when the Blue Dot is released.
        
        The function should accept 0 or 1 parameters, if the function accepts 1 parameter an 
        instance of BlueDotPosition will be returned representing where the Blue Dot was held 
        when it was released.
        """
        self._when_released = value

    @property
    def when_moved(self):
        """
        Returns the function which is called when the position the Blue Dot is pressed is moved. 
        """
        return self._when_moved

    @when_moved.setter
    def when_moved(self, value):
        """
        When set to a function it will cause the function to be run when the position of where
        the Blue Dot is pressed changes.
        
        The function should accept 0 or 1 parameters, if the function accepts 1 parameter an 
        instance of BlueDotPosition will be returned representing the new position of where the 
        Blue Dot is held.
        """
        self._when_moved = value

    @property 
    def when_client_connects(self):
        """
        Returns the function which is called when a Blue Dot connects. 
        """
        return self._when_client_connects

    @when_client_connects.setter
    def when_client_connects(self, value):
        """
        When set to a function it will cause the function to be run when a Blue Dot connects.
        """
        self._when_client_connects = value

    @property 
    def when_client_disconnects(self):
        """
        Returns the function which is called when a Blue Dot disconnects. 
        """
        return self._when_client_disconnects

    @when_client_disconnects.setter
    def when_client_disconnects(self, value):
        """
        When set to a function it will cause the function to be run when a Blue Dot disconnects.
        """
        self._when_client_disconnects = value

    @property
    def print_messages(self):
        """
        When set to ``True`` results in messages relating to the status of the bluetooth server
        to be printed.
        """
        return self._print_messages

    @print_messages.setter
    def print_messages(self, value):
        self._print_messages = value

    def start(self):
        """
        Start the BluetoothServer if it is not already running. By default the server is started at
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
                auto_start = False)

    def stop(self):
        """
        Stop the bluetooth server.
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
            Number of seconds to wait for a Blue Dot to be pressed, if ``None`` (the default), 
            it will wait indefinetly.
        """
        return self._is_pressed_event.wait(timeout)

    def wait_for_release(self, timeout = None):
        """
        Waits until a Blue Dot is released. 
        Returns ``True`` if the Blue Dot was released. 

        :param float timeout:
            Number of seconds to wait for a Blue Dot to be released, if ``None`` (the default), 
            it will wait indefinetly.
        """
        return self._is_released_event.wait(timeout)

    def wait_for_move(self, timeout = None):
        """
        Waits until the position where the Blue Dot is pressed is moved. 
        Returns ``True`` if the position pressed on the Blue Dot was moved. 

        :param float timeout:
            Number of seconds to wait for the position that the Blue Dot is pressed to move, if ``None`` (the default), 
            it will wait indefinetly.
        """
        return self._is_moved_event.wait(timeout)

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
            self.when_client_connects()

    def _client_disconnected(self):
        self._is_connected_event.clear()
        self._print_message("Client disconnected")
        if self.when_client_disconnects:
            self.when_client_disconnects()
        
    def _data_received(self, data):
        #add the data received to the buffer
        self._data_buffer += data
        
        #get any full commands ended by \n
        last_command = self._data_buffer.rfind("\n")
        if last_command != -1:
            commands = self._data_buffer[:last_command].split("\n")
            self._process_commands(commands)
            #remove the processed commands from the buffer
            self._data_buffer = self._data_buffer[last_command + 1:]

    def _process_commands(self, commands):
        
        for command in commands:
            operation, x, y = command.split(",")
            self._position = BlueDotPosition(x, y)
        
            #dot released
            if operation == "0":
                self._is_pressed_event.clear()
                self._is_released_event.set()
                self._is_moved_event.clear()
                if self.when_released:
                    if len(getargspec(self.when_released).args) == 0:
                        self.when_released()
                    else:
                        self.when_released(self._position)
    
            #dot pressed
            elif operation == "1":
                self._is_pressed_event.set()
                self._is_released_event.clear()
                self._is_moved_event.clear()
                if self.when_pressed:
                    if len(getargspec(self.when_pressed).args) == 0:
                        self.when_pressed()
                    else:
                        self.when_pressed(self._position)

            #dot pressed position moved
            elif operation == "2":
                self._is_moved_event.set()
                if self.when_moved:
                    self.when_moved(self._position)
                self._is_moved_event.clear()
                
    def _print_message(self, message):
        if self.print_messages:
            print(message)
