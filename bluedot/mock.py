import sys
from .server import BluetoothServer
from .dot import BlueDot

if sys.version_info[0] > 2:
    def string_to_bytes(data):
        return bytes(data, encoding="ascii")
else:
    def string_to_bytes(data):
        return bytes(data)

class MockBluetoothServer(BluetoothServer):
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
        if not self._client_connected:
            self._client_connected = True
            self._client_info = (client_address, self.port)
            #call the call back
            if self.when_client_connects:
                self._when_client_connects()
                
    def mock_client_disconnected(self):
        if self._client_connected:
            self._client_info = None
            if self._when_client_disconnects:
                self._when_client_disconnects()
                
    def mock_blue_dot_pressed(self, x, y):
        if self._client_connected:
            self._data_received_callback(string_to_bytes("1,{},{}\n".format(x, y)))
            #self._data_received_callback(bytes("1,{},{}\n".format(x, y)))
            #self._data_received_callback(bytes("1,{},{}\n".format(x, y)))
    
    def mock_blue_dot_released(self, x, y):
        if self._client_connected:
            self._data_received_callback(string_to_bytes("0,{},{}\n".format(x, y)))
            #self._data_received_callback(bytes("0,{},{}\n".format(x, y), encoding="ascii"))

    def mock_blue_dot_moved(self, x, y):
        if self._client_connected:
            self._data_received_callback(string_to_bytes("3,{},{}\n".format(x, y)))

class MockBlueDot(BlueDot):
    """
    MockBlueDot inherits from BlueDot but overrides create server, to create
    a MockBluetoothServer which can be used for testing.
    """
    def _create_server(self):
        self._server = MockBluetoothServer(
                self._data_received, 
                when_client_connects = self._client_connected,
                when_client_disconnects = self._client_disconnected,
                device = self.device,
                port = self.port)