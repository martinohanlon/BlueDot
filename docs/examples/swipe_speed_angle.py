from bluedot import BlueDot
from signal import pause

def swiped(swipe):
    print("Swiped")
    print("speed={}".format(swipe.speed))
    print("angle={}".format(swipe.angle))
    print("distance={}".format(swipe.distance))

bd = BlueDot()
bd.when_swiped = swiped

pause()
