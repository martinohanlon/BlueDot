from bluedot import BlueDot
from signal import pause

def bd1_pressed():
    print("BlueDot 1 pressed")

def bd2_pressed():
    print("BlueDot 2 pressed")

bd1 = BlueDot(port = 1)
bd2 = BlueDot(port = 2)

bd1.when_pressed = bd1_pressed
bd2.when_pressed = bd2_pressed

pause()
