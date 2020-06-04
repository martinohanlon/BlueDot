from bluedot import BlueDot
from signal import pause

bd = BlueDot()
bd.resize(3,3)

def increase_matrix():
    bd.resize(bd._cols + 1, bd._rows + 1)
    bd._send_cell_config(2, 2, "#ff0000ff", False, False, True)

bd.when_pressed = increase_matrix

pause()