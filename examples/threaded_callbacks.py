from bluedot import BlueDot
from time import sleep
from signal import pause
bd = BlueDot()

def pressed():
    print("pressed - waiting")
    sleep(3)
    print("pressed - complete")

def released():
    print("released")

bd.set_when_pressed(pressed, background=True)
bd.when_released = released

pause()
