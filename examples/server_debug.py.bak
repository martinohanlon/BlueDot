from bluedot.btcomm import BluetoothServer
from time import sleep
from signal import pause

def data_received(data):
    print("recv - {}".format(data))
    server.send(data)

def client_connected():
    print("client connected")

def client_disconnected():
    print("client disconnected")

print("init")
server = BluetoothServer(
    data_received,
    auto_start = False,
    when_client_connects = client_connected,
    when_client_disconnects = client_disconnected)

print("starting")
server.start()
print(server.server_address)
print("waiting for connection")

try:
    pause()
except KeyboardInterrupt as e:
    print("cancelled by user")
finally:
    print("stopping")
    server.stop()
print("stopped")
