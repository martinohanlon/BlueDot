from bluedot import BlueDot
from signal import pause

def swiped(swipe):
    if swipe.up:
        print("up")
    elif swipe.down:
        print("down")
    elif swipe.left:
        print("left")
    elif swipe.right:
        print("right")

bd = BlueDot()
bd.when_swiped = swiped

pause()
