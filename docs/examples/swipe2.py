from bluedot import BlueDot
from signal import pause

def swiped():
    print("Blue Dot swiped")

bd = BlueDot()
bd.when_swiped = swiped

pause()
