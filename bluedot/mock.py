from .btcomm import BluetoothServer, BluetoothAdapter
from .dot import BlueDot
from .threads import WrapThread


class MockBluetoothAdapter(BluetoothAdapter):
    def __init__(self, device = "hci0"):
        self._device = device
        self._address = "00:00:00:00:00:00"
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
    and :meth:`stop` to create a :class:`MockBluetoothServer` which can
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

        self._device = device
        self._adapter = MockBluetoothAdapter(self._device)

        self._data_received_callback = data_received_callback
        self._port = port
        self._encoding = encoding
        self._power_up_device = power_up_device
        self._when_client_connects = when_client_connects
        self._when_client_disconnects = when_client_disconnects

        self._running = False
        self._client_connected = False
        self._server_sock = None
        self._client_info = None
        self._client_sock = None

    def start(self):
        self._running = True

    def stop(self):
        self._running = False

    def mock_client_connected(self, client_address = "11:11:11:11:11:11"):
        """
        Simulates a client connected to the :class:`~.btcomm.BluetoothServer`.

        :param string client_address:
            The mock client mac address, defaults to '11:11:11:11:11:11'
        """
        if not self._client_connected:
            self._client_connected = True
            self._client_info = (client_address, self.port)
            #call the call back
            if self.when_client_connects:
                self._when_client_connects()

    def mock_client_disconnected(self):
        """
        Simulates a client disconnecting from the
        :class:`~.btcomm.BluetoothServer`.
        """
        if self._client_connected:
            self._client_connected = False
            self._client_info = None
            if self._when_client_disconnects:
                self._when_client_disconnects()

    def mock_client_sending_data(self, data):
        """
        Simulates a client sending data to the
        :class:`~.btcomm.BluetoothServer`.
        """
        if self._client_connected:
            self._data_received_callback(data)


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
                port = self.port)

    def mock_client_connected(self, client_address = "11:11:11:11:11:11"):
        """
        Simulates a client connecting to the Blue Dot.

        :param string client_address:
            The mock client mac address, defaults to '11:11:11:11:11:11'
        """
        self._server.mock_client_connected(client_address)

    def mock_client_disconnected(self):
        """
        Simulates a client disconnecting from the Blue Dot.
        """
        self._server.mock_client_disconnected()

    def mock_blue_dot_pressed(self, x, y):
        """
        Simulates the Blue Dot being pressed.

        :param int x:
            The x position where the mock Blue Dot was pressed

        :param int y:
            The y position where the mock Blue Dot was pressed
        """
        self._server.mock_client_sending_data("1,{},{}\n".format(x, y))

    def mock_blue_dot_released(self, x, y):
        """
        Simulates the Blue Dot being released.

        :param int x:
            The x position where the mock Blue Dot was released

        :param int y:
            The y position where the mock Blue Dot was released
        """
        self._server.mock_client_sending_data("0,{},{}\n".format(x, y))

    def mock_blue_dot_moved(self, x, y):
        """
        Simulates the Blue Dot being moved.

        :param int x:
            The x position where the mock Blue Dot was moved too

        :param int y:
            The y position where the mock Blue Dot was moved too
        """
        self._server.mock_client_sending_data("2,{},{}\n".format(x, y))

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
        #imported here, so pygame is only a pre-requisite for the mock app
        import pygame

        pygame.init()
        screen = pygame.display.set_mode((200,200))
        pygame.display.set_caption("Blue Dot")

        clock = pygame.time.Clock()

        circle_centre = (100, 100)
        circle_radius = 100
        circle_rect = pygame.draw.circle(screen, (0,0, 255), circle_centre, circle_radius, 0)

        self.mock_client_connected()

        running = True
        while running:
            clock.tick(50)

            # get all events
            ev = pygame.event.get()

            # proceed events
            for event in ev:

                # handle mouse
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP or (event.type == pygame.MOUSEMOTION and self.is_pressed):
                    pos = pygame.mouse.get_pos()

                    if circle_rect.collidepoint(pos):
                        x = (pos[0] - circle_centre[0]) / circle_radius
                        x = round(x, 4)
                        y = ((pos[1] - circle_centre[1]) / circle_radius) * -1
                        y = round(y, 4)

                        if event.type == pygame.MOUSEBUTTONDOWN:
                            self.mock_blue_dot_pressed(x,y)

                        elif event.type == pygame.MOUSEBUTTONUP:
                            self.mock_blue_dot_released(x,y)

                        elif event.type == pygame.MOUSEMOTION:
                            self.mock_blue_dot_moved(x,y)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

                if event.type == pygame.QUIT:
                    running = False

                if self._mock_app_thread.stopping.is_set():
                    running = False

            pygame.display.update()

        self.mock_client_disconnected()

        pygame.quit()
