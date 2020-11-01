from bluedot import BlueDot
from signal import pause

def pressed(pos):
    print("button {}.{} pressed".format(pos.col, pos.row))

bd = BlueDot(cols=3, rows=1)
bd[1,0].visible = False
bd.when_pressed = pressed

pause()