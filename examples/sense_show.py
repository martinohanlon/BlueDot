#!/usr/bin/env python3
"""
This module is an example of driving the sense hat with blue dot.

It shows an array of dots on the ui each corresponding to a pixel on the 16x16 array on the sense hat.

Tapping on a dot toggles that pixel, it is very satisfying.
"""

from sense_hat import SenseHat
from time import sleep
from bluedot import BlueDot
from signal import pause

sense = SenseHat()

# draw an array of dots corresponding to the pixels on the Sense HAT
bd=BlueDot(cols=8, rows=10)
for x in range(8):
    for y in range(8):
        bd[x,y].color=(50,50,50)

# add in dots for the controls
for x in range(8):
    for y in range(8,10):
        bd[x,y].color=(255,255,255)
        bd[x,y].visible = False

# set up the brush dot that defines what color will be painted

brush=(0,0,0)
brush_dot = bd[0,9]
brush_dot.visible = True

def change_brush(color):
    global brush
    print(f"change_brush{color}")
    brush_dot.color = color
    brush=color
    print(f'Brush: {brush}')

# set up the pallet of colours you can change the brush to

pallet = [(248, 248, 248), (248, 0, 248), (248, 0, 0), (248, 248, 0), (0, 248, 0), (0, 248, 248), (0, 0, 248)]
change_brush(pallet[-1])

def change_brush_pressed(pos):
    print('change_brush')
    color_idx = pos.col-1
    color = pallet[color_idx]
    change_brush(color)

for idx, color in enumerate(pallet):
    dot = bd[idx+1, 9]
    dot.color=color
    dot.when_pressed = change_brush_pressed
    dot.visible = True
    dot.square = True

# handle interactions with the pixels

def pressed(pos):
    "handler for bd.when_pressed that toggles a pixel"
    
    print("dot {}.{} pressed".format(pos.col, pos.row))
    
    if pos.row > 7:
        return
    
    pixel = sense.get_pixel(pos.col, pos.row)
    print(f'Current pixel:{pixel}, toggling brush color: {brush}')

    if tuple(pixel) == brush: # is the pixel set to the brush?
        print(f'Pixel already set to {brush}, turning off.')
        sense.set_pixel(pos.col, pos.row, 0,0,0)
        bd[pos.col, pos.row].color = (50,50,50)
    else:
        print(f'Pixel not set to {brush}, setting.')
        sense.set_pixel(pos.col, pos.row, brush[0], brush[1], brush[2])
        bd[pos.col, pos.row].color = brush

bd.when_pressed = pressed

# blink blue to signal ready

sense.clear(0,0,255)
sleep(1)
sense.clear(0,0,0)

# pause to keep the script running

pause()