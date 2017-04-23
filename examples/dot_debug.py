from bluedot import BlueDot
from time import sleep, time

dot = BlueDot(auto_start_server = False)
dot.allow_pairing()

def pressed(pos):
    print("Pressed: x={} y={} angle={} distance={} middle={} top={} bottom={} left={} right={} time={}".format(pos.x, pos.y, pos.angle, pos.distance, pos.middle, pos.top, pos.bottom, pos.left, pos.right, time()))

def released():
    print("Released: x={} y={}".format(dot.position.x, dot.position.y))

def moved(pos):
    print("Moved: x={} y={}".format(pos.x, pos.y))

def client_connected():
    print("client connected")

def client_disconnected():
    print("client disconnected")

dot.when_client_connects = client_connected
dot.when_client_disconnects = client_disconnected
dot.when_pressed = pressed
dot.when_released = released
dot.when_moved = moved
dot.start()

try:
    while True:
        sleep(0.1)
finally:
    dot.stop()
