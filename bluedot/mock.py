from .btcomm import BluetoothServer, BluetoothClient, BluetoothAdapter
from .dot import BlueDot
from .threads import WrapThread
from .constants import PROTOCOL_VERSION

CLIENT_NAME = "Mock client"

class MockBluetoothAdapter(BluetoothAdapter):
    def __init__(self, device = "mock0", address = "00:00:00:00:00:00"):
        self._device = device
        self._address = address
        self._powered = True
        self._discoverable = False
        self._pairable = False
        self._pairing_thread = None

    @property
    def powered(self):
        return self._powered

    @powered.setter
    def powered(self, value):
        self._powered = value

    @property
    def discoverable(self):
        return self._discoverable

    @discoverable.setter
    def discoverable(self, value):
        self._discoverable = value

    @property
    def pairable(self):
        return self._pairable

    @pairable.setter
    def pairable(self, value):
        self._pairable = value

    @property
    def paired_devices(self):
        return [["01:01:01:01:01:01", "mock_device_1"], ["02:02:02:02:02:02", "mock_device_2"]]


class MockBluetoothServer(BluetoothServer):
    """
    :class:`MockBluetoothServer` inherits from
    :class:`~.btcomm.BluetoothServer` but overrides ``__init__``, :meth:`start`
    , :meth:`stop` and :meth:`send_raw` to create a :class:`MockBluetoothServer` which can
    be used for testing and debugging.
    """
    def __init__(self,
        data_received_callback,
        auto_start = True,
        device = "mock0",
        port = 1,
        encoding = "utf-8",
        power_up_device = False,
        when_client_connects = None,
        when_client_disconnects = None):

        super(MockBluetoothServer, self).__init__(
            data_received_callback,
            auto_start,
            device,
            port,
            encoding,
            power_up_device,
            when_client_connects,
            when_client_disconnects)

        self._mock_client = None

    def start(self):
        self._running = True

    def stop(self):
        self._running = False

    def mock_client_connected(self, mock_client = None):
        """
        Simulates a client connected to the :class:`~.btcomm.BluetoothServer`.
        
        :param MockBluetoothClient mock_client:
            The mock client to interact with, defaults to `None`. If `None`, 
            client address is set to '99:99:99:99:99:99'
        """
        self._mock_client = mock_client

        if not self._client_connected:
            if self._mock_client is None:
                client_address = "99:99:99:99:99:99"
            else:
                client_address = self._mock_client.adapter.address
            self._client_connected = True
            self._client_info = (client_address, self.port)
            #call the call back
            if self.when_client_connects:
                WrapThread(target=self.when_client_connects).start()

    def mock_client_disconnected(self):
        """
        Simulates a client disconnecting from the
        :class:`~.btcomm.BluetoothServer`.
        """
        if self._client_connected:
            self._client_connected = False
            self._client_info = None
            if self._when_client_disconnects:
                WrapThread(target=self.when_client_disconnects).start()

    def mock_client_sending_data(self, data):
        """
        Simulates a client sending data to the
        :class:`~.btcomm.BluetoothServer`.
        """
        if self._client_connected:
            self._data_received_callback(data)

    def _send_data(self, data):
        if self._mock_client is not None:
            # call the data received callback
            if self._encoding:
                data = data.decode(self._encoding)
            self._mock_client.mock_server_sending_data(data)

    def _setup_adapter(self, device):
        self._adapter = MockBluetoothAdapter(device)


class MockBluetoothClient(BluetoothClient):
    """
    :class:`MockBluetoothClient` inherits from
    :class:`~.btcomm.BluetoothClient` but overrides ``__init__``, :meth:`connect`
    and :meth:`send_raw` to create a :class:`MockBluetoothServer` which can
    be used for testing and debugging.

    Note - the `server` parameter should be an instance of :class:`MockBluetoothServer`.
    """
    def __init__(self,
        server,
        data_received_callback,
        port = 1,
        device = "mock1",
        encoding = "utf-8",
        power_up_device = False,
        auto_connect = True):

        super(MockBluetoothClient, self).__init__(
            server,
            data_received_callback,
            port,
            device,
            encoding,
            power_up_device,
            auto_connect)

    def connect(self):
        """
        Connect to a Bluetooth server.
        """
        self._server.mock_client_connected(self)
        self._connected = True

    def disconnect(self):
        """
        Disconnect from a Bluetooth server.
        """
        self._server.mock_client_disconnected()
        self._connected = False

    def mock_server_sending_data(self, data):
        """
        Simulates a server sending data to the
        :class:`~.btcomm.BluetoothClient`.
        """
        if self._connected:
            self._data_received_callback(data)

    def _send_data(self, data):
        # send data to the server
        # call the data received callback
        if self._encoding:
            data = data.decode(self._encoding)
        self._server.mock_client_sending_data(data)

    def _setup_adapter(self, device):
        self._adapter = MockBluetoothAdapter(device, address = "11:11:11:11:11:11")

class MockBlueDot(BlueDot):
    """
    :class:`MockBlueDot` inherits from :class:`BlueDot` but overrides
    :meth:`_create_server`, to create a :class:`~.mock.MockBluetoothServer`
    which can be used for testing and debugging.
    """
    def _create_server(self):
        self._server = MockBluetoothServer(
                self._data_received,
                when_client_connects = self._client_connected,
                when_client_disconnects = self._client_disconnected,
                device = self.device,
                port = self.port,
                power_up_device = self._power_up_device,
                auto_start = False)

    def mock_client_connected(self):
        """
        Simulates a client connecting to the Blue Dot.

        :param string client_address:
            The mock client mac address, defaults to '11:11:11:11:11:11'
        """
        self._server.mock_client_connected()
        # send protocol version to server
        self._server.mock_client_sending_data("3,{},{}\n".format(PROTOCOL_VERSION, CLIENT_NAME))

    def mock_client_disconnected(self):
        """
        Simulates a client disconnecting from the Blue Dot.
        """
        self._server.mock_client_disconnected()

    def mock_blue_dot_pressed(self, col, row, x, y):
        """
        Simulates the Blue Dot being pressed.

        :param int col:
            The column position of the button

        :param int row:
            The row position of the button 

        :param int x:
            The x position where the button was pressed

        :param int y:
            The y position where the button was pressed
        """
        self._server.mock_client_sending_data("1,{},{},{},{}\n".format(col, row, x, y))

    def mock_blue_dot_released(self, col, row, x, y):
        """
        Simulates the Blue Dot being released.

        :param int col:
            The column position of the button

        :param int row:
            The row position of the button 

        :param int x:
            The x position where the button was released

        :param int y:
            The y position where the button was released

        """
        self._server.mock_client_sending_data("0,{},{},{},{}\n".format(col, row, x, y))

    def mock_blue_dot_moved(self, col, row, x, y):
        """
        Simulates the Blue Dot being moved.

        :param int col:
            The column position of the button

        :param int row:
            The row position of the button 

        :param int x:
            The x position where the button was moved too

        :param int y:
            The y position where the button was moved too

        """
        self._server.mock_client_sending_data("2,{},{},{},{}\n".format(col, row, x, y))

    def launch_mock_app(self):
        """
        Launches a mock Blue Dot app.

        The mock app reacts to mouse clicks and movement and calls the mock blue
        dot methods to simulates presses.

        This is useful for testing, allowing you to interact with Blue Dot without
        having to script mock functions.

        The mock app uses pygame which will need to be installed.
        """
        self._mock_app_thread = WrapThread(target=self._launch_mock_app)
        self._mock_app_thread.start()

    def _launch_mock_app(self):
        # imported here, so pygame is only a pre-requisite for the mock app
        from .app import BlueDotClient, ButtonScreen

        class MockBlueDotClient(BlueDotClient):
            def _run(self):
                button_screen = MockButtonScreen(self._screen, self._font, self._device, self._server, self._port, self._width, self._height)
                button_screen.run()

        class MockButtonScreen(ButtonScreen):
            def _connect(self):
                self.bt_client = MockBluetoothClient(self.server, self._data_received, device = self.device, auto_connect = True)

        MockBlueDotClient("mock2", self._server, self._port, None, None, None)
