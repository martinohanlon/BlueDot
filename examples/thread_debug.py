from bluedot import BlueDot
from time import sleep
from signal import pause

def pressed(pos):
    print("pressed {} {}".format(pos.x, pos.y))
    sleep(2)
    print("pressed ended {} {}".format(pos.x, pos.y))    

def moved(pos):
    print("moved {} {}".format(pos.x, pos.y))

def released(pos):
    print("released {} {}".format(pos.x, pos.y))

bd = BlueDot()
bd.when_pressed = pressed
bd.when_released = released
bd.when_moved = moved

pause()