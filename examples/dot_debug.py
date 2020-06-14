from bluedot import BlueDot
from time import sleep, time

dot = BlueDot(auto_start_server = False)
dot.resize(1,2)
dot.allow_pairing()

def pressed(pos):
    print("Pressed: x={} y={} angle={} distance={} middle={} top={} bottom={} left={} right={} time={}".format(pos.x, pos.y, pos.angle, pos.distance, pos.middle, pos.top, pos.bottom, pos.left, pos.right, time()))

def pressed_two(pos):
    print("Second dot:" + pos)

def released():
    print("Released: x={} y={}".format(dot.position.x, dot.position.y))

def moved(pos):
    print("Moved: x={} y={}".format(pos.x, pos.y))

def swiped(swipe):
    print("Swiped: up={} down={} left={} right={} speed={}".format(swipe.up, swipe.down, swipe.left, swipe.right, swipe.speed))

def double_presed(pos):
    print("Double pressed: x={} y={}".format(pos.x, pos.y))

def client_connected():
    print("connected callback")

def client_disconnected():
    print("disconnected callback")

dot.when_client_connects = client_connected
dot.when_client_disconnects = client_disconnected
dot.when_pressed = pressed
dot.when_released = released
dot.when_moved = moved
dot.when_swiped = swiped
dot.when_double_pressed = double_presed
dot[0,1].when_pressed = pressed_two

dot.start()

dot.wait_for_press()
print("wait for press")
dot.wait_for_move()
print("wait for move")
dot.wait_for_release()
print("wait for release")
dot.wait_for_double_press()
print("wait for double press")
dot.wait_for_swipe()
print("wait for swipe")

try:
    while True:
        sleep(0.1)
finally:
    dot.stop()
