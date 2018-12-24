from bluedot import BlueDot
# color zero can be installed using sudo pip3 install colorzero
from colorzero import Color
from signal import pause

def on(pos):
    hue = (pos.angle + 180) / 360
    c = Color(h=hue, s=1, v=pos.distance)
    bd.color = c.rgb_bytes

def off():
    bd.color = "blue"

bd = BlueDot()
bd.when_pressed = on
bd.when_moved = on
bd.when_released = off

pause()