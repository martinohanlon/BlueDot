from signal import pause
from bluedot import BlueDot
bd = BlueDot()

def double_pressed():
    print("double pressed")

bd.when_double_pressed = double_pressed

pause()