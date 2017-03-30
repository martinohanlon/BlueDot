from bluedot import BlueDot
from picamera import PiCamera
from signal import pause

dot = BlueDot()
cam = PiCamera()

def take_picture():
    cam.capture("pic.jpg")

dot.when_pressed = take_picture
pause()
