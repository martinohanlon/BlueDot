from bluedot import MockBlueDot
from signal import pause

def say_hello():
    print("Hello World")

bd = MockBlueDot()
bd.when_pressed = say_hello

bd.launch_mock_app()
pause()
