from bluedot.btcomm import BluetoothClient
from datetime import datetime
from time import sleep
from signal import pause

def data_received(data):
    print("recv - {}".format(data))

print("Connecting")
#devpi - pi3 ceed
c = BluetoothClient("devpi", data_received)
#c = BluetoothClient("devpi", None)
#c = BluetoothClient("B8:27:EB:68:C2:85", data_received)
#piscreen dongle
#c = BluetoothClient("00:15:83:15:A3:10", data_received)

print("Sending")
try:
    while True:
        c.send("hi {} \n".format(str(datetime.now())))
        sleep(1)
finally:
    c.disconnect()
    