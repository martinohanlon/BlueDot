from bluedot import BlueDot
from signal import pause

bd = BlueDot()

def increase_matrix():
    bd.resize(bd._cols + 1, bd._rows + 1)

bd.when_pressed = increase_matrix

pause()