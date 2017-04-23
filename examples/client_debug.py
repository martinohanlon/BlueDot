from bluedot.btcomm import BluetoothClient
from datetime import datetime
from time import sleep

#devpi - pi3 ceed
c = BluetoothClient("devpi")
#c = BluetoothClient("B8:27:EB:68:C2:85")
#piscreen dongle
#c = BluetoothClient("00:15:83:15:A3:10")

print("Powered {}, discoverable {}, pairable {}".format(c.adapter.powered, c.adapter.discoverable, c.adapter.pairable))
print("Pairing")
c.adapter.allow_pairing()
print("Powered {}, discoverable {}, pairable {}".format(c.adapter.powered, c.adapter.discoverable, c.adapter.pairable))

print("Connecting & sending")
c.connect()
c.send("hi \n")
c.send(str(datetime.now()))