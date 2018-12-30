from bluedot import BlueDot
from bluedot.colors import RED, GREEN

from signal import pause

def change_dot(pos):
    if pos.top:
        if bd.color == "red":
            bd.color = GREEN
        else:
            bd.color = "#ff0000"
    elif pos.bottom:
        if bd.border:
            bd.border = False
        else:
            bd.border = True
    elif pos.left:
        if bd.visible:
            bd.visible = False
        else:
            bd.visible = True
    elif pos.right:
        if bd.square:
            bd.square = False
        else:
            bd.square = True

bd = BlueDot()
bd.color="pink"
bd.border = False
bd.square = True
bd.when_pressed = change_dot

pause()