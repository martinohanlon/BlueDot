from bluedot import BlueDot
from signal import pause
import sys

def bd0_pressed():
    print("bd0 pressed")

def bd1_pressed():
    print("bd1 pressed")

bd0 = BlueDot(device = "hci0")
bd1 = BlueDot(device = "hci1")
bd0.when_pressed = bd0_pressed
bd1.when_pressed = bd1_pressed

pause()

#testing all channels
"""
for c in range(1,60):
    try:
        bd = BlueDot(port = c)
        bd.stop()
    except:
        print("failed to create bd on port {}".format(c))
        print(sys.exc_info()[1])
pause()
"""
