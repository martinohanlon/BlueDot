from bluedot import BlueDot, COLORS
from signal import pause
from random import choice

bd = BlueDot()
bd.resize(1,2)

def pressed(pos):
    print("Pressed      : {}".format(pos))

def moved(pos):
    print("Moved        : {}".format(pos))

def released(pos):
    print("Released     : {}".format(pos))

def double_press(pos):
    print("Double press : {}".format(pos))

def increase_matrix():
    bd.resize(bd._cols + 1, bd._rows + 1)
    # bd._send_cell_config(2, 2, "#ff0000ff", False, False, True)

def change_color():
    # increase_matrix()
    # bd[bd.cols - 1, bd.rows - 1].color = "green"
    for c in range(bd.cols):
        for r in range(bd.rows):
            bd[c,r].color = choice(list(COLORS.keys()))

    #print(bd.cells)

change_color()

# bd.when_pressed = increase_matrix
bd[0,0].when_pressed = pressed
bd[0,0].when_moved = moved
bd[0,0].when_released = released
bd[0,0].when_double_pressed = double_press

bd.when_pressed = pressed
bd.when_moved = moved
bd.when_released = released
bd.when_double_pressed = double_press


pause()