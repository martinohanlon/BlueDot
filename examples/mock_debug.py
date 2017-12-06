from bluedot.mock import MockBlueDot
from time import sleep, time

mbd = MockBlueDot(auto_start_server = False)

def pressed(pos):
    print("Pressed: x={} y={} angle={} distance={} middle={} top={} bottom={} left={} right={} time={}".format(pos.x, pos.y, pos.angle, pos.distance, pos.middle, pos.top, pos.bottom, pos.left, pos.right, time()))

def released():
    print("Released: x={} y={}".format(dot.position.x, dot.position.y))
    print()

def moved(pos):
    print("Moved: x={} y={}".format(pos.x, pos.y))
    
mbd.when_pressed = pressed
mbd.when_released = released
mbd.when_moved = moved
mbd.start()
mbd.mock_client_connected()
mbd.wait_for_connection()

try:
    while True:
        mbd.mock_blue_dot_pressed(1.0,1.0)
        mbd.mock_blue_dot_moved(0.5,1.0)
        mbd.mock_blue_dot_released(0.5,1.0)
        sleep(0.1)
finally:
    mbd.mock_client_disconnected()
    mbd.stop()
