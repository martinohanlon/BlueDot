from bluedot.mock import MockBluetoothClient, MockBluetoothServer

def s_client_connected():
    print("s: c connected")
    
def s_data_received(data):
    print("s: recv - {}".format(data))
    
print("s: creating")
s = MockBluetoothServer(
    s_data_received,
    when_client_connects=s_client_connected
    )

def c_data_received(data):
    print("c: recv - {}".format(data))

print("c: creating")
c = MockBluetoothClient(
    s, 
    c_data_received
    )

c.send("hi")
s.send("bye")
