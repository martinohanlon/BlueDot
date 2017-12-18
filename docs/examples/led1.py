import os
from bluedot import BlueDot
from gpiozero import LED

bd = BlueDot()
led = LED(27)

bd.wait_for_press()
led.on()

bd.wait_for_release()
led.off()
