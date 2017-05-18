from bluedot import BlueDot, BlueDotSwipe
from signal import pause

bd = BlueDot()

print("waiting for swipe")
bd.wait_for_swipe()
print("swiped")

def released():
    swipe = BlueDotSwipe(bd.interaction)
    if not swipe.valid:
        print("Invalid swipe - speed {}".format(swipe.speed))

def valid_swipe(swipe):
    #swipe = BlueDotSwipe(bd.interaction)
    #print("valid {} duration {} distance {} angle {}".format(swipe.valid, swipe.interaction.duration, swipe.distance, swipe.angle))
    #print("up {} down {} left {} right {}".format(swipe.up, swipe.down, swipe.left, swipe.right))
    if swipe.up:
        print("UP {}".format(swipe.speed))
    elif swipe.down:
        print("DOWN {}".format(swipe.speed))
    elif swipe.left:
        print("LEFT {}".format(swipe.speed))
    elif swipe.right:
        print("RIGHT {}".format(swipe.speed))

bd.when_released = released
bd.when_swiped = valid_swipe

pause()