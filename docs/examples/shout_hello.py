from bluedot import BlueDot
from signal import pause

def shout_hello():
    print("HELLO")

bd = BlueDot()
bd.when_double_pressed = shout_hello

pause()
