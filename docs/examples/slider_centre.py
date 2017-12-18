from bluedot import BlueDot
from signal import pause

def show_percentage(pos):
    percentage = round(pos.distance * 100, 2)
    print("{}%".format(percentage))

bd = BlueDot()
bd.when_moved = show_percentage

pause()
