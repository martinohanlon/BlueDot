from bluedot import BlueDot
from signal import pause

def pressed_1(pos):
    print("button 1 pressed")

def pressed_2(pos):
    print("button 2 pressed")

bd = BlueDot(cols=2, rows=1)

bd[0,0].when_pressed = pressed_1
bd[1,0].when_pressed = pressed_2

pause()