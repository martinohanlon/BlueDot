from bluedot import BlueDot
from signal import pause

bd = BlueDot()
bd.resize(3,3)

def increase_matrix():
    bd.resize(bd._cols + 1, bd._rows + 1)
    # bd._send_cell_config(2, 2, "#ff0000ff", False, False, True)

def change_color():
    bd.cells[(1,1)].color = "yellow"
    bd.cells[(1,0)].border = True
    bd.cells[(0,1)].visible = False
    
    print(bd.cells)

# bd.when_pressed = increase_matrix
bd.when_pressed = change_color

pause()