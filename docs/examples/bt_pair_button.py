from bluedot import BlueDot
from gpiozero import Button
from signal import pause

bd = BlueDot()
button = Button(27)

button.when_pressed = bd.allow_pairing

pause()
