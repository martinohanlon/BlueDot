from bluedot import BlueDot
from signal import pause

def pressed(pos):
    print("button {}.{} pressed".format(pos.col, pos.row))

bd = BlueDot(cols=2)
bd.when_pressed = pressed

pause()