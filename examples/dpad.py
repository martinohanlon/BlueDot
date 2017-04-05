from bluedot import BlueDot
from signal import pause

def dpad(pos):
    if pos.top:
        print("up")
    elif pos.bottom:
        print("down")
    elif pos.left:
        print("left")
    elif pos.right:
        print("right")

bd = BlueDot()
bd.when_pressed = dpad
bd.when_moved = dpad

pause()