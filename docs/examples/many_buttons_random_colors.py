from bluedot import BlueDot, COLORS
from random import choice
from signal import pause

def pressed(pos):
    print("button {}.{} pressed".format(pos.col, pos.row))

bd = BlueDot(cols=2, rows=5)
bd.when_pressed = pressed

for button in bd.buttons:
    button.color = choice(list(COLORS.values()))

pause()