from bluedot import BlueDot
from turtle import Turtle

bd = BlueDot()

while True:
    bd.wait_for_press()
    print("pressed")

    bd.wait_for_move()
    print("moved")
    
    bd.wait_for_release()
    print("released")

    bd.wait_for_double_press()
    print("double press")
    
    bd.wait_for_swipe()
    print("swipe")
    
    
    
