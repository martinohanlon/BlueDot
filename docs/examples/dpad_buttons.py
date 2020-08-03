from bluedot import BlueDot
from signal import pause

bd = BlueDot(cols=3, rows=3)
#bd[1,0].color = "red"
bd.square = True
bd.color = "purple"
print(bd.color)
print(bd[0,0].color)

bd[0,0].visible = False
bd[2,0].visible = False
bd[0,2].visible = False
bd[2,2].visible = False
bd[1,1].visible = False

pause()