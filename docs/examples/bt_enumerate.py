from bluedot import BlueDot
bd = BlueDot()

devices = bd.paired_devices
for d in devices:
    device_address = d[0]
    device_name = d[1]
