from bluedot import BlueDot, COLORS
from signal import pause
from random import choice

bd = BlueDot()
bd.resize(3,3)

def increase_matrix():
    bd.resize(bd._cols + 1, bd._rows + 1)
    # bd._send_cell_config(2, 2, "#ff0000ff", False, False, True)

def change_color():
    increase_matrix()
    # bd[bd.cols - 1, bd.rows - 1].color = "green"
    for c in range(bd.cols):
        for r in range(bd.rows):
            bd[c,r].color = choice(list(COLORS.keys()))

    #print(bd.cells)
    
# bd.when_pressed = increase_matrix
bd.when_pressed = change_color

pause()