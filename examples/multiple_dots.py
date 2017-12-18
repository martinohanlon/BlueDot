from bluedot import BlueDot
from signal import pause
import sys

def bd0_pressed():
    print("bd0 pressed")

def bd1_pressed():
    print("bd1 pressed")

# 2 bluetooth adapters are required, each must be paired to a remote
bd0 = BlueDot(device = "hci0")
bd1 = BlueDot(device = "hci1")
bd0.when_pressed = bd0_pressed
bd1.when_pressed = bd1_pressed

pause()
