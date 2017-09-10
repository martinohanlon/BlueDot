import socket
import sys
from time import sleep

from .utils import register_spp, get_mac, get_adapter_powered_status, get_adapter_discoverable_status, get_adapter_pairable_status, get_paired_devices, device_pairable, device_discoverable, device_powered, string_to_bytes

from .threads import WrapThread

if sys.version_info[0] > 2:
    BLUETOOTH_EXCEPTIONS = (BlockingIOError, ConnectionResetError, TimeoutError)
else:
    BLUETOOTH_EXCEPTIONS = (IOError)

BLUETOOTH_TIMEOUT = 0.01

class BluetoothAdapter():
    """
    Represents and allows interaction with a Bluetooth Adapter.

    The following example will get the bluetooth adapter, print its powered status
    and any paired devices::

        a = BluetoothAdapter()
        print("Powered = {}".format(a.powered))
        print(a.paired_devices)

    :param string device:
        The bluetooth device to be used, the default is ``hci0``, if your device 
        only has 1 bluetooth adapter this shouldn't need to be changed.
    """
    def __init__(self, device = "hci0"):
        self._device = device
        self._address = get_mac(self._device)
        self._pairing_thread = None

    @property
    def device(self):
        """
        The bluetooth device name. This defaults to hci0.
        """
        return self._device
    
    @property
    def address(self):
        """
        The mac address of the bluetooth adapter.
        """
        return self._address

    @property
    def powered(self):
        """
        Set to ``True`` to power on the bluetooth adapter.

        Depending on how bluetooth has been powered down, you may need to use 
        rfkill to unblock bluetooth to give permission to bluez to power on bluetooth::

            sudo rfkill unblock bluetooth
        """
        return get_adapter_powered_status(self._device)

    @powered.setter
    def powered(self, value):
        device_powered(self._device, value)

    @property
    def discoverable(self):
        """
        Set to ``True`` to make the bluetooth adapter discoverable.
        """
        return get_adapter_discoverable_status(self._device)

    @discoverable.setter
    def discoverable(self, value):
        device_discoverable(self._device, value)

    @property
    def pairable(self):
        """
        Set to ``True`` to make the bluetooth adapter pairable.
        """
        return get_adapter_pairable_status(self._device)

    @pairable.setter
    def pairable(self, value):
        device_pairable(self._device, value)

    @property
    def paired_devices(self):
        """
        Returns a list of devices paired with this adapater 
        ``((device_mac_address, device_name), (device_mac_address, device_name))``::
        
            a = BluetoothAdapter()
            devices = a.paired_devices
            for d in devices:
                device_address = d[0]
                device_name = d[1]

        """
        return get_paired_devices(self._device)

    def allow_pairing(self, timeout = 60):
        """
        Put the adapter into discoverable and pairable mode.

        :param int timeout:
            The time in seconds the adapter will remain pairable. If set to ``None``
            the device will be discoverable and pairable indefinetly. 
        """
        #if a pairing thread is already running, stop it and restart
        if self._pairing_thread:
            if self._pairing_thread.is_alive:
                self._pairing_thread.stop()
        
        #make the adapter pairable
        self.pairable = True
        self.discoverable = True
        
        if timeout != None:
            #start the pairing thread
            self._pairing_thread = WrapThread(target=self._expire_pairing, args=(timeout, ))
            self._pairing_thread.start()

    def _expire_pairing(self, timeout):
        #wait till the timeout or the thread is stopped
        self._pairing_thread.stopping.wait(timeout)
        self.discoverable = False
        self.pairable = False

class BluetoothServer():
    """
    Creates a Bluetooth server which will allow connections and accept incoming 
    RFCOMM serial data.

    When data is received by the server it is passed to a callback function
    which must be specified at initiation.

    The following example will create a bluetooth server which will wait for a 
    connection and print any data it receives and send it back to the client::
    
        from bluedot.btcomm import BluetoothServer
        from signal import pause

        def data_received(data):
            print(data)
            s.send(data)

        s = BluetoothServer(data_received)
        pause()

    :param data_received_callback:
        A function reference should be passed, this function will be called when
        data is received by the server.  The function should accept a single parameter
        which when called will hold the data received. Set to ``None`` if  received 
        data is not required.

    :param bool auto_start:
        If ``True`` (the default), the bluetooth server will be automatically started
        on initialisation, if ``False``, the method ``start`` will need to be called
        before connections will be accepted.

    :param string device:
        The bluetooth device the server should use, the default is ``hci0``, if
        your device only has 1 bluetooth adapter this shouldn't need to be changed.

    :param int port:
        The bluetooth port the server should use, the default is ``1``.

    :param string encoding:
        The encoding standard to be used when sending and receiving byte data. The default is 
        ``utf-8``.  If set to ``None`` no encoding is done and byte data types should be used.

    :param bool power_up_device:
        If ``True``, the bluetooth device will be powered up (if required) when the 
        server starts. The default is ``False``. 
        
        Depending on how bluetooth has been powered down, you may need to use rfkill 
        to unblock bluetooth to give permission to bluez to power on bluetooth::

            sudo rfkill unblock bluetooth

    :param when_client_connects:
        A function reference which will be called when a client connects. If ``None``
        (the default), no notification will be given when a client connects

    :param when_client_disconnects:
        A function reference which will be called when a client disconnects. If ``None``
        (the default), no notification will be given when a client disconnects

    """
    def __init__(self, 
        data_received_callback, 
        auto_start = True, 
        device = "hci0", 
        port = 1,
        encoding = "utf-8",
        power_up_device = False,
        when_client_connects = None, 
        when_client_disconnects = None):

        self._device = device
        self._adapter = BluetoothAdapter(self._device)

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
        
        self._conn_thread = None

        if auto_start:
            self.start()
    
    @property
    def device(self):
        """
        The bluetooth device the server is using. This defaults to hci0.
        """
        return self.adapter.device

    @property
    def adapter(self):
        """
        A BluetoothAdapter object which represents the bluetooth device 
        the server is using.
        """
        return self._adapter

    @property
    def port(self):
        """
        The port the server is using. This defaults to 1.
        """
        return self._port

    @property
    def encoding(self):
        """
        The encoding standard the server is using. This defaults to ``utf-8``.
        """
        return self.encoding

    @property
    def running(self):
        """
        Returns a ``True`` if the server is running.
        """
        return self._running

    @property
    def server_address(self):
        """
        The mac address of the device the server is using.
        """
        return self.adapter.address

    @property
    def client_address(self):
        """
        The mac address of the client connected to the server. Returns 
        ``None`` if no client is connected.
        """
        if self._client_info:
            return self._client_info[0]
        else:
            return None

    @property
    def client_connected(self):
        """
        Returns ``True`` if a client is connected.
        """
        return self._client_connected

    @property
    def data_received_callback(self):
        """
        Sets or returns the function which is called when data is received by the server. 

        The function should accept a single parameter which when called will hold
        the data received. Set to ``None`` if received data is not required.
        """
        return self._data_received_callback

    @data_received_callback.setter
    def data_received_callback(self, value):
        self._data_received_callback = value

    @property
    def when_client_connects(self):
        """
        Sets or returns the function which is called when a client connects. 
        """
        return self._when_client_connects

    @when_client_connects.setter
    def when_client_connects(self, value):
        self._when_client_connects = value

    @property
    def when_client_disconnects(self):
        """
        Sets or returns the function which is called when a client disconnects. 
        """
        return self._when_client_disconnects

    @when_client_disconnects.setter
    def when_client_disconnects(self, value):
        self._when_client_disconnects = value

    def start(self):
        """
        Starts the Bluetooth server if its not already running. The server needs to be started before
        connections can be made.
        """
        if not self._running:

            if self._power_up_device:
                self.adapter.powered = True

            if not self.adapter.powered:
                raise Exception("Bluetooth device {} is turned off".format(self.adapter.device))

            #register the serial port profile with bluetooth
            register_spp(self._port)

            #start bluetooth server
            #open the bluetooth socket
            self._server_sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
            self._server_sock.settimeout(BLUETOOTH_TIMEOUT)
            try:
                self._server_sock.bind((self.server_address, self.port))
            except (socket.error, OSError) as e:
                if str(e) == "[Errno 98] Address already in use":
                    print("Bluetooth address {} is already in use - is the server already running?".format(self.server_address))
                raise e
            self._server_sock.listen(1)

            #wait for client connection
            self._conn_thread = WrapThread(target=self._wait_for_connection)
            self._conn_thread.start()

            self._running = True

    def stop(self):
        """
        Stops the Bluetooth server if its running.
        """
        if self._running:
            if self._conn_thread:
                self._conn_thread.stop()
                self._conn_thread = None

    def send(self, data):
        """
        Send data to a connected bluetooth client

        :param string data:
            The data to be sent.
        """
        if self._client_connected:
            if self._encoding:
                data = string_to_bytes(data, self._encoding)
            try:
                self._client_sock.send(data)
            except BLUETOOTH_EXCEPTIONS as e:
                self._handle_bt_error(e)

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
                if self._data_received_callback:
                    if self._encoding:
                        data = data.decode(self._encoding)
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
    """
    Creates a Bluetooth client which can send data to a server using RFCOMM Serial Data.

    The following example will create a bluetooth client which will connect to a paired 
    device called ``raspberrypi``, send ``helloworld`` and print any data is receives::
    
        from bluedot.btcomm import BluetoothClient
        from signal import pause
        
        def data_received(data):
            print(data)

        c = BluetoothClient("raspberrypi", data_received)
        c.send("helloworld")

        pause()
    
    :param string server:
        The server name ("raspberrypi") or server mac address 
        ("11:11:11:11:11:11") to connect too.

        The server must be a paired device.

    :param data_received_callback:
        A function reference should be passed, this function will be called when
        data is received by the client.  The function should accept a single parameter
        which when called will hold the data received. Set to ``None`` if data 
        received is not required.

    :param int port:
        The bluetooth port the client should use, the default is ``1``

    :param string device:
        The bluetooth device to be used, the default is ``hci0``, if your device 
        only has 1 bluetooth adapter this shouldn't need to be changed.

    :param string encoding:
        The encoding standard to be used when sending and receiving byte data. The default is 
        ``utf-8``.  If set to ``None`` no encoding is done and byte data types should be used.

    :param bool power_up_device:
        If ``True``, the bluetooth device will be powered up (if required) when the 
        server starts. The default is ``False``. 
        
        Depending on how bluetooth has been powered down, you may need to use rfkill 
        to unblock bluetooth to give permission to bluez to power on bluetooth::

            sudo rfkill unblock bluetooth

    :param bool auto_connect:
        If ``True`` (the default), the bluetooth client will automatically try to
        connect to the server at initialisation, if ``False``, the method ``connect`` 
        will need to be called.

    """
    def __init__(self, 
        server,
        data_received_callback,
        port = 1,
        device = "hci0", 
        encoding = "utf-8",
        power_up_device = False,
        auto_connect = True):

        self._device = device
        self._server = server
        self._data_received_callback = data_received_callback
        self._port = port
        self._power_up_device = power_up_device
        self._encoding = encoding

        self._adapter = BluetoothAdapter(self._device)

        self._connected = False
        self._client_sock = None

        self._conn_thread = None

        if auto_connect:
            self.connect()

    @property
    def device(self):
        """
        The bluetooth device the client is using. This defaults to hci0.
        """
        return self.adapter.device

    @property
    def server(self):
        """
        The server name ("raspberrypi") or server mac address 
        ("11:11:11:11:11:11") to connect too.
        """
        return self._server

    @property
    def port(self):
        """
        The port the client is using. This defaults to 1.
        """
        return self._port

    @property
    def adapter(self):
        """
        A BluetoothAdapter object which represents the bluetooth device 
        the client is using.
        """
        return self._adapter

    @property
    def encoding(self):
        """
        The encoding standard the client is using. The default is ``utf-8``. 
        """
        return self._encoding

    @property
    def client_address(self):
        """
        The mac address of the device being used.
        """
        return self.adapter.address

    @property
    def connected(self):
        """
        Returns ``True`` when connected.
        """
        return self._connected

    @property
    def data_received_callback(self):
        """
        Sets or returns the function which is called when data is received by the client. 
        
        The function should accept a single parameter which when called will hold
        the data received. Set to ``None`` if data received is not required.
        """
        return self._data_received_callback

    @data_received_callback.setter
    def data_received_callback(self, value):
        self._data_received_callback = value

    def connect(self):
        """
        Connect to a bluetooth server.
        """
        if not self._connected:

            if self._power_up_device:
                self.adapter.powered = True

            if not self.adapter.powered:
                raise Exception("Bluetooth device {} is turned off".format(self.adapter.device))

            #try and find the server name or mac address in the paired devices list
            server_mac = None
            for device in self.adapter.paired_devices:
                if self._server == device[0] or self._server == device[1]:
                    server_mac = device[0]
                    break
            if server_mac == None:
                raise Exception("Server {} not found in paired devices".format(self._server))
            
            #create a socket
            self._client_sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
            self._client_sock.bind((self.adapter.address, self._port))
            self._client_sock.connect((server_mac, self._port))
        
            self._connected = True 
        
            self._conn_thread = WrapThread(target=self._read)
            self._conn_thread.start()

    def disconnect(self):
        """
        Disconnect from a bluetooth server.
        """
        if self._connected:
            
            #stop the connection thread
            if self._conn_thread:
                self._conn_thread.stop()
                self._conn_thread = None

            #close the socket
            try:
                self._client_sock.close()
            finally:
                self._client_sock = None
                self._connected = False
        
    def send(self, data):
        """
        Send data to a bluetooth server

        :param string data:
            The data to be sent.
        """
        if self._connected:
            if self._encoding:
                data = string_to_bytes(data, self._encoding)
            try:
                self._client_sock.send(data)
            except BLUETOOTH_EXCEPTIONS as e:
                self._handle_bt_error(e)
            
    def _read(self):
        #read until the client is stopped or the client disconnects
        while not self._conn_thread.stopping.is_set() and self._connected:
            #read data from bluetooth socket
            data = ""
            try:
                data = self._client_sock.recv(1024, socket.MSG_DONTWAIT)
            except BLUETOOTH_EXCEPTIONS as e:
                self._handle_bt_error(e)
            if len(data) > 0:
                #print("received [%s]" % data)
                if self._data_received_callback:
                    if self._encoding:
                        data = data.decode(self._encoding)
                    self.data_received_callback(data)
            sleep(BLUETOOTH_TIMEOUT)

    def _handle_bt_error(self, bt_error):
        #'resource unavailable' is when data cannot be read because there is nothing in the buffer
        if str(bt_error) == "[Errno 11] Resource temporarily unavailable":
            return
        #'connection reset' is caused when the client disconnects
        if str(bt_error) == "[Errno 104] Connection reset by peer":
            self._connected = False
            return
        #'conection timeout' is caused when the server can no longer connect to read from the client
        # (perhaps the client has gone out of range)
        if str(bt_error) == "[Errno 110] Connection timed out":
            self._connected = False
            return
        raise bt_error
