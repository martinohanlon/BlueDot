import pytest
from bluedot.btcomm import BluetoothAdapter, BluetoothServer, BluetoothClient
from threading import Event

# have we got 2 adapters
try:
    bta0 = BluetoothAdapter("hci0")
    bta1 = BluetoothAdapter("hci1")
except Exception as e:
    pytest.skip(str(e) + " - skipping test", allow_module_level = True)

# is adapter 0 paired with adapter 1 and vice versa
paired = False
for device in bta0.paired_devices:
    if device[0] == bta1.address:
        paired = True
if not paired:
    pytest.skip("hci0 is not paired with hci1", allow_module_level = True)

paired = False
for device in bta1.paired_devices:
    if device[0] == bta0.address:
        paired = True
if not paired:
    pytest.skip("hci1 is not paired with hci0", allow_module_level = True)

def test_server_default_values():
    def data_received(data):
        pass

    bts = BluetoothServer(data_received)
    assert bts.data_received_callback == data_received
    assert bts.device == "hci0"
    assert bts.server_address == bta0.address
    assert bts.running
    assert bts.port == 1
    assert bts.encoding == "utf-8"
    assert bts.when_client_connects == None
    assert bts.when_client_disconnects == None 

    bts.stop()

def test_server_alt_values():
    def data_received(data):
        pass

    def when_client_connects():
        pass

    def when_client_disconnects():
        pass

    bts = BluetoothServer(
        data_received, 
        device = "hci1", 
        auto_start = False, 
        port = 2, 
        encoding = None, 
        when_client_connects = when_client_connects, 
        when_client_disconnects = when_client_disconnects)

    assert bts.data_received_callback == data_received
    assert bts.device == "hci1"
    assert bts.server_address == bta1.address
    assert not bts.running
    assert bts.port == 2
    assert bts.encoding == None
    assert bts.when_client_connects == when_client_connects
    assert bts.when_client_disconnects == when_client_disconnects

def test_server_start_stop():

    bts = BluetoothServer(None, auto_start = False)

    bts.start()
    assert bts.running

    bts.stop()
    assert not bts.running

def test_client_default_values():
    def data_received(data):
        pass

    bts = BluetoothServer(data_received, device = "hci1")
    btc = BluetoothClient(bta1.address, data_received)
    
    assert btc.data_received_callback == data_received
    assert btc.device == "hci0"
    assert btc.server == bta1.address
    assert btc.client_address == bta0.address
    assert btc.connected
    assert btc.port == 1
    assert btc.encoding == "utf-8"

    btc.disconnect()
    bts.stop()

def test_client_alt_values():
    def data_received(data):
        pass

    bts = BluetoothServer(None, port = 2, encoding = None)
    btc = BluetoothClient(bta0.address, data_received, device = "hci1", auto_connect = False, port = 2, encoding = None)
    
    assert btc.data_received_callback == data_received
    assert btc.device == "hci1"
    assert btc.client_address == bta1.address
    assert not btc.connected
    assert btc.port == 2
    assert btc.encoding == None

    btc.connect()
    assert btc.connected
    
    btc.disconnect()
    assert not btc.connected

    bts.stop()

def test_client_connect_disconnect():

    client_connected = Event()
    client_disconnected = Event()

    def when_client_connects():
        client_connected.set()

    def when_client_disconnects():
        client_disconnected.set()

    bts = BluetoothServer(None)
    btc = BluetoothClient(bta0.address, None, device = "hci1", auto_connect = False)
    bts.when_client_connects = when_client_connects
    bts.when_client_disconnects = when_client_disconnects

    btc.connect()
    assert btc.connected
    assert bts.client_address == btc.client_address
    assert client_connected.wait(1)
    
    btc.disconnect()
    assert not btc.connected
    assert client_disconnected.wait(1)

    bts.stop()

def test_send_receive():

    data_received_at_server = Event()
    data_received_at_client = Event()
    
    def data_received_server(data):
        assert data == "hiserver"
        data_received_at_server.set()

    def data_received_client(data):
        assert data == "hiclient"
        data_received_at_client.set()

    bts = BluetoothServer(data_received_server, device = "hci0")
    btc = BluetoothClient(bta0.address, data_received_client, device = "hci1")

    btc.send("hiserver")
    assert data_received_at_server.wait(1)
    bts.send("hiclient")
    assert data_received_at_server.wait(1)
    
    btc.disconnect()
    bts.stop()
