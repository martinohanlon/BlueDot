import sys
from .server import BluetoothServer
from .dot import BlueDot
from .threads import WrapThread

if sys.version_info[0] > 2:
    def string_to_bytes(data):
        return bytes(data, encoding="ascii")
else:
    def string_to_bytes(data):
        return bytes(data)

class MockBluetoothServer(BluetoothServer):
    """
    MockBluetoothServer inherits from BluetoothServer but overrides __init__, .start 
    and .stop to create a MockBluetoothServer which can be used for testing and debugging.
    """
    def __init__(self, 
        data_received_callback, 
		auto_start = True, 
		device = "mock0", 
        port = 1,
		when_client_connects = None, 
		when_client_disconnects = None):
        
        self._data_received_callback = data_received_callback
        self._device = device
        self._port = port
        self._when_client_connects = when_client_connects
        self._when_client_disconnects = when_client_disconnects
        
        self._running = False
        self._server_address = "00:00:00:00:00:00"
        self._client_connected = False
        self._client_info = None
            
    def start(self):
        self._running = True
        
    def stop(self):
        self._running = False
        
    def mock_client_connected(self, client_address = "11:11:11:11:11:11"):
        """
        Simulates a client connected to the BluetoothServer. 

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
        Simulates a client disconnecting from the BluetoothServer. 
        """
        if self._client_connected:
            self._client_connected = False
            self._client_info = None
            if self._when_client_disconnects:
                self._when_client_disconnects()

    def mock_client_sending_data(self, data):
        """
        Simulates a client sending data to the BluetoothServer. 
        """
        if self._client_connected:
            self._data_received_callback(data)

class MockBlueDot(BlueDot):
    """
    MockBlueDot inherits from BlueDot but overrides ._create_server, to create
    a MockBluetoothServer which can be used for testing and debugging.
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
        Simulates a client connecting to the BlueDot. 

        :param string client_address:
            The mock client mac address, defaults to '11:11:11:11:11:11'
        """
        self._server.mock_client_connected(client_address)
                
    def mock_client_disconnected(self):
        """
        Simulates a client disconnecting from the BlueDot. 
        """
        self._server.mock_client_disconnected()
                
    def mock_blue_dot_pressed(self, x, y):
        """
        Simulates the blue dot being pressed. 

        :param int x:
            The x position where the mock blue dot was pressed

        :param int y:
            The y position where the mock blue dot was pressed    
        """
        self._server.mock_client_sending_data(string_to_bytes("1,{},{}\n".format(x, y)))

    def mock_blue_dot_released(self, x, y):
        """
        Simulates the blue dot being released. 

        :param int x:
            The x position where the mock blue dot was released

        :param int y:
            The y position where the mock blue dot was released   
        """
        self._server.mock_client_sending_data(string_to_bytes("0,{},{}\n".format(x, y)))

    def mock_blue_dot_moved(self, x, y):
        """
        Simulates the blue dot being moved. 

        :param int x:
            The x position where the mock blue dot was moved too

        :param int y:
            The y position where the mock blue dot was moved too  
        """
        self._server.mock_client_sending_data(string_to_bytes("3,{},{}\n".format(x, y)))

    def launch_mock_app(self):
        """
        Launches a mock Blue Dot app.
        
        The mock app reacts to mouse clicks and movement and calls the mock blue
        dot methods to simulates presses.
        
        This is useful for testing, allowing you to interact with BlueDot without
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

        circle_centre = (100, 100)
        circle_radius = 100
        circle_rect = pygame.draw.circle(screen, (0,0, 255), circle_centre, circle_radius, 0)
        
        self.mock_client_connected()

        running = True
        while running:
            # get all events
            ev = pygame.event.get()

            # proceed events
            for event in ev:

                # handle mouse
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP or (event.type == pygame.MOUSEMOTION and self.is_pressed):
                    pos = pygame.mouse.get_pos()
                    
                    if circle_rect.collidepoint(pos):
                        x = (pos[0] - circle_centre[0]) / circle_radius
                        y = ((pos[1] - circle_centre[1]) / circle_radius) * -1

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