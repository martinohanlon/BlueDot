from bluedot import BlueDot
from signal import pause

def up():
    print("up")

def down():
    print("down")

def left():
    print("left")

def right():
    print("right")

bd = BlueDot(cols=3, rows=3)
bd.color = "gray"
bd.square = True

bd[0,0].visible = False
bd[2,0].visible = False
bd[0,2].visible = False
bd[2,2].visible = False
bd[1,1].visible = False

bd[1,0].when_pressed = up
bd[1,2].when_pressed = down
bd[0,1].when_pressed = left
bd[2,1].when_pressed = right

pause()