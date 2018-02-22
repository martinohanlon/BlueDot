from bluedot import BlueDot
from signal import pause

def client_connected():
    print("callback - a blue dot client connected")

def client_disconnected():
    print("callback - the blue dot client disconnected")

bd = BlueDot()
bd.when_client_connects = client_connected
bd.when_client_disconnects = client_disconnected

pause()