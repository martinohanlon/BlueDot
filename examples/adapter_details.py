from bluedot import BlueDot
bd = BlueDot()

print("Address {}".format(bd.adapter.address))
print("powered {}".format(bd.adapter.powered))
print("discoverable {}".format(bd.adapter.discoverable))
print("pairable {}".format(bd.adapter.pairable))

print("paired devices:")
paired_devices = bd.paired_devices
for d in paired_devices:
    print(" mac {} name {}".format(d[0], d[1]))

