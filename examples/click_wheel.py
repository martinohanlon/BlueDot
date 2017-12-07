from bluedot import BlueDot
from signal import pause

def moved(pos):
    last_pos = bd.interaction.positions[-2]
    
    if last_pos.distance > 0.5 and pos.distance > 0.5:

        segments = 32
        deg_per_seg = (360 / segments)

        last_seg = int((last_pos.angle + 180) / deg_per_seg) + 1
        current_seg = int((pos.angle + 180) / deg_per_seg) + 1

        diff = last_seg - current_seg
        value = 0
        if diff == -1:
            value = 1
        elif diff == 1:
            value = -1
        elif diff == (segments - 1):
            value = 1
        elif diff == (1 - segments):
            value = -1

        if value != 0:
            print(value)
    
    #print("{} : {} : {}".format(last_seg, current_seg, value))

bd = BlueDot()
bd.when_moved = moved

pause()