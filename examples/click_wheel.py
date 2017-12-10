from bluedot import BlueDot
from signal import pause

count = 0

def rotated(rotation):
    global count
    count += rotation.value

    print("{} {} {}".format(count, rotation.clockwise, rotation.anti_clockwise))
    
bd = BlueDot()
bd.when_rotated = rotated

pause()
