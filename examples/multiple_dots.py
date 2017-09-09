from bluedot import BlueDot
from signal import pause
import sys
bd1 = BlueDot(port = 2)
#bd2 = BlueDot(port = 2)
#bd2 = BlueDot(port = 3)
pause()
#test all channels
"""
for c in range(1,60):
    try:
        bd = BlueDot(port = c)
        bd.stop()
    except:
        print("failed to create bd on port {}".format(c))
        print(sys.exc_info()[1])
pause()
"""