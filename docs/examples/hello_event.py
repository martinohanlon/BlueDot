from bluedot import BlueDot
from signal import pause

def say_hello():
    print("Hello World")

bd = BlueDot()
bd.when_pressed = say_hello

pause()
