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

def button_A():
    print("A")

def button_B():
    print("B")

bd = BlueDot(cols=5, rows=3)

# dpad buttons
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

# buttons
bd[3,0].visible = False
bd[4,0].visible = False
bd[3,2].visible = False
bd[4,2].visible = False

bd[3,1].color = "blue"
bd[3,1].square = False
bd[3,1].when_pressed = button_A

bd[4,1].color = "red"
bd[4,1].when_pressed = button_B

pause()