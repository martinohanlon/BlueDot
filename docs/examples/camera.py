from bluedot import BlueDot
from picamera import PiCamera
from signal import pause

bd = BlueDot()
cam = PiCamera()

def take_picture():
    cam.capture("pic.jpg")

bd.when_pressed = take_picture

pause()
