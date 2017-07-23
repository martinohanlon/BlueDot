import time
import bluedot
bd = bluedot.BlueDot()

def bd_pressed() -> None:
    print("pressed")

bd.when_pressed = bd_pressed
while True:
    time.sleep(1.0)
