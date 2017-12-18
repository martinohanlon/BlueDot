from bluedot import MockBlueDot

def say_hello():
    print("Hello World")

bd = MockBlueDot()
bd.when_pressed = say_hello

bd.mock_client_connected()
bd.mock_blue_dot_pressed(0,0)
