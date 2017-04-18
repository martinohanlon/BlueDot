import socket
import sys
from time import sleep

from utils import get_mac, get_adapter_powered_status, get_adapter_discoverable_status, get_adapter_pairable_status, get_paired_devices, device_pairable, device_discoverable

if sys.version_info[0] > 2:
    BLUETOOTH_EXCEPTIONS = (BlockingIOError, ConnectionResetError, TimeoutError)
else:
    BLUETOOTH_EXCEPTIONS = (IOError)

BLUETOOTH_TIMEOUT = 0.01

class BluetoothAdapter():
    def __init__(self, device = "hci0"):
        self._device = device
        self._address = get_mac(self._device)

    @property
    def device(self):
        return self._device
    
    @property
    def address(self):
        return self._address

    @property
    def powered(self):
        return get_adapter_powered_status(self._device)

    @property
    def discoverable(self):
        return get_adapter_discoverable_status(self._device)

    @discoverable.setter
    def discoverable(self, value):
        device_discoverable(self._device, value)

    @property
    def pairable(self):
        return get_adapter_pairable_status(self._device)

    @pairable.setter
    def pairable(self, value):
        device_pairable(self._device, value)

    @property
    def paired_devices(self):
        return get_paired_devices(self._device)

class BluetoothServer():

    def __init__(self, 
        data_received_callback, 
        auto_start = True, 
        device = "hci0", 
        port = 1,
        when_client_connects = None, 
        when_client_disconnects = None):

        self._adapter = BluetoothAdapter(self.device)

        self._data_received_callback = data_received_callback
        self._port = port
        self._when_client_connects = when_client_connects
        self._when_client_disconnects = when_client_disconnects

        self._running = False
        self._client_connected = False
        self._server_sock = None
        self._client_info = None
        self._client_sock = None
        
        self._conn_thread = None

        if not self.adapter.powered:
            raise Exception("Bluetooth device {} is turned off".format(self.adapter.device))

        if auto_start:
            self.start()
    
    @property
    def device(self):
        return self.adapter.device

    @property
    def adapter(self):
        return self._adapter

    @property
    def port(self):
        return self._port

    @property
    def running(self):
        return self._running

    @property
    def server_address(self):
        return self.adapter.address

    @property
    def client_address(self):
        if self._client_info:
            return self._client_info[0]
        else:
            return None

    @property
    def client_connected(self):
        return self._client_connected

    @property
    def data_received_callback(self):
        return self._data_received_callback

    @data_received_callback.setter
    def data_received_callback(self, value):
        self._data_received_callback = value

    @property
    def when_client_connects(self):
        return self._when_client_connects

    @when_client_connects.setter
    def when_client_connects(self, value):
        self._when_client_connects = value

    @property
    def when_client_disconnects(self):
        return self._when_client_disconnects

    @when_client_disconnects.setter
    def when_client_disconnects(self, value):
        self._when_client_disconnects = value

    def start(self):
        self._running = True

        #register the serial port profile with bluetooth
        register_spp()

        #start bluetooth server
        #open the bluetooth socket
        self._server_sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
        self._server_sock.settimeout(BLUETOOTH_TIMEOUT)
        self._server_sock.bind((self.server_address, self.port))
        self._server_sock.listen(1)

        #wait for client connection
        self._conn_thread = WrapThread(target=self._wait_for_connection)
        self._conn_thread.start()
		
    def stop(self):
        if self._running:
            if self._conn_thread:
                self._conn_thread.stop()
                self._conn_thread = None

    def _wait_for_connection(self):
        #keep going until the server is stopped
        while not self._conn_thread.stopping.is_set():
            #wait for connection
            self._client_connected = False
            while not self._conn_thread.stopping.is_set() and not self._client_connected:
                try:
                    self._client_sock, self._client_info = self._server_sock.accept()
                    self._client_connected = True
                except socket.timeout as e:
                    self._handle_bt_error(e)

            #did a client connect?
            if self._client_connected:
                #call the call back
                if self.when_client_connects:
                    self.when_client_connects()
                
                #read data
                self._read()

        #server has been stopped
        self._server_sock.close()
        self._server_sock = None
        self._running = False

    def _read(self):
        #read until the server is stopped or the client disconnects
        while not self._conn_thread.stopping.is_set() and self._client_connected:
            #read data from bluetooth socket
            data = ""
            try:
                data = self._client_sock.recv(1024, socket.MSG_DONTWAIT)
            except BLUETOOTH_EXCEPTIONS as e:
                self._handle_bt_error(e)
            if len(data) > 0:
                #print("received [%s]" % data)
                self.data_received_callback(data)
            sleep(BLUETOOTH_TIMEOUT)

        #close the client socket
        self._client_sock.close()
        self._client_sock = None
        self._client_info = None
        self._client_connected = False

    def _handle_bt_error(self, bt_error):
        #'timed out' is caused by the wait_for_connection loop
        if str(bt_error) == "timed out":
            return
        #'resource unavailable' is when data cannot be read because there is nothing in the buffer
        if str(bt_error) == "[Errno 11] Resource temporarily unavailable":
            return
        #'connection reset' is caused when the client disconnects
        if str(bt_error) == "[Errno 104] Connection reset by peer":
            self._client_connected = False
            if self.when_client_disconnects:
                self.when_client_disconnects()
            return
        #'conection timeout' is caused when the server can no longer connect to read from the client
        # (perhaps the client has gone out of range)
        if str(bt_error) == "[Errno 110] Connection timed out":
            self._client_connected = False
            if self.when_client_disconnects:
                self.when_client_disconnects()
            return
        raise bt_error

class BluetoothClient():

    def __init__(self, device = "hci0"):
        self._device = device

        self._adapter = BluetoothAdapter(self._device)

        self._connected = False
        self._client_sock = None

        if not self.adapter.powered:
            raise Exception("Bluetooth device {} is turned off".format(self.adapter.device))

    @property
    def device(self):
        return self._device

    @property
    def adapter(self):
        return self._adapter

    @property
    def client_address(self):
        return self.adapter.address

    @property
    def connected(self):
        return self._connected

    def connect(self, server_address, port = 1):
        if not self._connected:
            self._client_sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
            self._client_sock.bind((self.adapter.address, port))
            self._client_sock.connect((server_address, port))
            self._connected = True 
        
    def disconnect(self):
        if not self._connected:
            try:
                self._client_sock.close()
            finally:
                self._client_sock = None
                self._connected = False
        
    def send(self, data):
        #going to need some python 2 / 3 compatability work with bytes
        self._client_sock.send(bytes(data, encoding = 'UTF-8'))
      
print(get_paired_devices("hci0"))
#device_discoverable("hci0", True)
#device_discoverable("hci0", False)
#device_pairable("hci0", True)
#device_pairable("hci0", False)

c = BluetoothClient()

#pizerow
#c.connect("B8:27:EB:CA:C7:71")
#piscreen dongle
#c.connect("00:15:83:15:A3:10")
#pi3 ceed
c.connect("B8:27:EB:68:C2:85")

c.send("hi")

#errors
# ConnectionRefusedError: [Errno 111] Connection refused

# cant find connection
# OSError: [Errno 113] No route to host