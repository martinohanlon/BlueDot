from bluedot import MockBlueDot, BlueDotSwipe, BlueDotRotation
from time import sleep
from threading import Event

def test_default_values():
    mbd = MockBlueDot()
    assert mbd.device == "hci0"
    assert mbd.port == 1
    assert mbd.running

    assert mbd.print_messages
    assert mbd.double_press_time == 0.3
    assert mbd.rotation_segments == 8

    assert mbd.when_client_connects == None
    assert mbd.when_client_disconnects == None
    assert mbd.when_pressed == None
    assert mbd.when_double_pressed == None
    assert mbd.when_moved == None
    assert mbd.when_released == None
    assert mbd.when_swiped == None

def test_modify_values():
    mbd = MockBlueDot(device = "hci1", port = 2, auto_start_server = False, print_messages = False)
    assert mbd.device == "hci1"
    assert mbd.port == 2
    assert not mbd.running

    assert not mbd.print_messages
    mbd.print_messages = True
    assert mbd.print_messages

    assert mbd.double_press_time == 0.3
    mbd.double_press_time = 0.4
    assert mbd.double_press_time == 0.4

    assert mbd.rotation_segments == 8
    mbd.rotation_segments = 16
    assert mbd.rotation_segments == 16

def test_start_stop():
    mbd = MockBlueDot(auto_start_server = False)
    assert not mbd.running
    mbd.start()
    assert mbd.running
    mbd.stop()
    assert not mbd.running

def test_connect_disconnect():
    mbd = MockBlueDot()
    assert not mbd.is_connected
    mbd.mock_client_connected()
    assert mbd.wait_for_connection(1)
    assert mbd.is_connected
    mbd.mock_client_disconnected()
    assert not mbd.is_connected

def test_when_connect_disconnect():
    mbd = MockBlueDot()

    event_connect = Event()
    mbd.when_client_connects = lambda: event_connect.set()

    event_disconnect = Event()
    mbd.when_client_disconnects = lambda: event_disconnect.set()

    assert not event_connect.is_set()
    mbd.mock_client_connected()
    assert event_connect.is_set()

    assert not event_disconnect.is_set()
    mbd.mock_client_disconnected()
    assert event_disconnect.is_set()

def test_pressed_moved_released():
    mbd = MockBlueDot()
    mbd.mock_client_connected()

    #initial value
    assert not mbd.is_pressed
    assert mbd.value == 0

    #pressed
    mbd.mock_blue_dot_pressed(0,0)
    assert mbd.is_pressed
    assert mbd.value == 1

    #released
    mbd.mock_blue_dot_released(0,0)
    assert not mbd.is_pressed
    assert mbd.value == 0

    #wait_for_press
    mbd.mock_blue_dot_pressed(0,0)
    assert mbd.wait_for_press(1)
    assert not mbd.wait_for_release(0)

    #wait_for_release
    mbd.mock_blue_dot_released(0,0)
    assert mbd.wait_for_release(1)
    assert not mbd.wait_for_press(0)

def test_when_pressed_moved_released():
    mbd = MockBlueDot()
    mbd.mock_client_connected()

    #when_pressed
    event_pressed = Event()
    mbd.when_pressed = lambda: event_pressed.set()

    #when_double_pressed
    event_double_pressed = Event()
    mbd.when_double_pressed = lambda: event_double_pressed.set()

    #when_moved
    event_moved = Event()
    mbd.when_moved = lambda: event_moved.set()

    #when_released
    event_released = Event()
    mbd.when_released = lambda: event_released.set()

    assert not event_pressed.is_set()
    mbd.mock_blue_dot_pressed(0,0)
    assert event_pressed.is_set()

    assert not event_moved.is_set()
    mbd.mock_blue_dot_moved(1,1)
    assert event_moved.is_set()

    assert not event_released.is_set()
    mbd.mock_blue_dot_released(0,0)
    assert event_released.is_set()

    assert not event_double_pressed.is_set()
    mbd.mock_blue_dot_pressed(0,0)
    assert event_double_pressed.is_set()

def test_position():
    mbd = MockBlueDot()
    mbd.mock_client_connected()

    mbd.mock_blue_dot_pressed(0,0)
    assert not mbd.position.top
    assert mbd.position.middle
    assert not mbd.position.bottom
    assert not mbd.position.left
    assert not mbd.position.right

    mbd.mock_blue_dot_moved(1,0)
    assert not mbd.position.top
    assert not mbd.position.middle
    assert not mbd.position.bottom
    assert not mbd.position.left
    assert mbd.position.right

    mbd.mock_blue_dot_moved(-1,0)
    assert not mbd.position.top
    assert not mbd.position.middle
    assert not mbd.position.bottom
    assert mbd.position.left
    assert not mbd.position.right

    mbd.mock_blue_dot_moved(0,1)
    assert mbd.position.top
    assert not mbd.position.middle
    assert not mbd.position.bottom
    assert not mbd.position.left
    assert not mbd.position.right

    mbd.mock_blue_dot_moved(0,-1)
    assert not mbd.position.top
    assert not mbd.position.middle
    assert mbd.position.bottom
    assert not mbd.position.left
    assert not mbd.position.right

    mbd.mock_blue_dot_moved(0.1234, -0.4567)
    assert mbd.position.x == 0.1234
    assert mbd.position.y == -0.4567

    mbd.mock_blue_dot_moved(1, 0)
    assert mbd.position.distance == 1
    assert mbd.position.angle == 90

def test_interaction():
    mbd = MockBlueDot()
    mbd.mock_client_connected()
    assert mbd.interaction == None

    mbd.mock_blue_dot_pressed(-1,0)
    assert mbd.interaction.active
    assert len(mbd.interaction.positions) == 1
    assert mbd.interaction.distance == 0
    assert mbd.interaction.pressed_position.x == -1
    assert mbd.interaction.pressed_position.y == 0
    assert mbd.interaction.current_position.x == -1
    assert mbd.interaction.current_position.y == 0
    assert mbd.interaction.previous_position == None
    assert mbd.interaction.released_position == None

    mbd.mock_blue_dot_moved(0,0)
    assert mbd.interaction.active
    assert len(mbd.interaction.positions) == 2
    assert mbd.interaction.distance == 1
    assert mbd.interaction.pressed_position.x == -1
    assert mbd.interaction.pressed_position.y == 0
    assert mbd.interaction.current_position.x == 0
    assert mbd.interaction.current_position.y == 0
    assert mbd.interaction.previous_position.x == -1
    assert mbd.interaction.previous_position.y == 0
    assert mbd.interaction.released_position == None

    mbd.mock_blue_dot_released(1,0)
    assert not mbd.interaction.active
    assert len(mbd.interaction.positions) == 3
    assert mbd.interaction.distance == 2
    assert mbd.interaction.pressed_position.x == -1
    assert mbd.interaction.pressed_position.y == 0
    assert mbd.interaction.current_position.x == 1
    assert mbd.interaction.current_position.y == 0
    assert mbd.interaction.previous_position.x == 0
    assert mbd.interaction.previous_position.y == 0
    assert mbd.interaction.released_position.x == 1
    assert mbd.interaction.released_position.y == 0

def test_swipe():
    mbd = MockBlueDot()
    mbd.mock_client_connected()

    #when_swiped
    event_swiped = Event()
    mbd.when_swiped = lambda: event_swiped.set()
    assert not event_swiped.is_set()

    #simulate swipe left to right
    mbd.mock_blue_dot_pressed(-1,0)
    mbd.mock_blue_dot_moved(0,0)
    mbd.mock_blue_dot_released(1,0)
    #check event
    assert event_swiped.is_set()
    #get the swipe
    swipe = BlueDotSwipe(mbd.interaction)
    assert swipe.right
    assert not swipe.left
    assert not swipe.up
    assert not swipe.down

    #right to left
    event_swiped.clear()
    mbd.mock_blue_dot_pressed(1,0)
    mbd.mock_blue_dot_moved(0,0)
    mbd.mock_blue_dot_released(-1,0)
    assert event_swiped.is_set()
    swipe = BlueDotSwipe(mbd.interaction)
    assert not swipe.right
    assert swipe.left
    assert not swipe.up
    assert not swipe.down

    #bottom to top
    event_swiped.clear()
    mbd.mock_blue_dot_pressed(0,-1)
    mbd.mock_blue_dot_moved(0,0)
    mbd.mock_blue_dot_released(0,1)
    assert event_swiped.is_set()
    swipe = BlueDotSwipe(mbd.interaction)
    assert not swipe.right
    assert not swipe.left
    assert swipe.up
    assert not swipe.down

    #top to bottom
    event_swiped.clear()
    mbd.mock_blue_dot_pressed(0,1)
    mbd.mock_blue_dot_moved(0,0)
    mbd.mock_blue_dot_released(0,-1)
    assert event_swiped.is_set()
    swipe = BlueDotSwipe(mbd.interaction)
    assert not swipe.right
    assert not swipe.left
    assert not swipe.up
    assert swipe.down

def test_rotation():
    mbd = MockBlueDot()
    mbd.mock_client_connected()

    event_rotated = Event()
    mbd.when_rotated = lambda: event_rotated.set()
    assert not event_rotated.is_set()

    #press the blue dot, no rotation
    mbd.mock_blue_dot_pressed(-0.1,1)
    assert not event_rotated.is_set()
    r = BlueDotRotation(mbd.interaction, mbd.rotation_segments)
    assert not r.valid
    assert r.value == 0
    assert not r.clockwise
    assert not r.anti_clockwise

    #rotate clockwise
    event_rotated.clear()
    mbd.mock_blue_dot_moved(0.1,1)
    assert event_rotated.is_set()
    r = BlueDotRotation(mbd.interaction, mbd.rotation_segments)
    assert r.value == 1
    assert r.valid
    assert r.clockwise
    assert not r.anti_clockwise

    #rotate anti-clockwise
    event_rotated.clear()
    mbd.mock_blue_dot_moved(-0.1,1)
    assert event_rotated.is_set()
    r = BlueDotRotation(mbd.interaction, mbd.rotation_segments)
    assert r.value == -1
    assert r.valid
    assert not r.clockwise
    assert r.anti_clockwise

def test_allow_pairing():
    mbd = MockBlueDot()
    assert not mbd.adapter.discoverable
    assert not mbd.adapter.pairable

    mbd.allow_pairing()
    assert mbd.adapter.discoverable
    assert mbd.adapter.pairable

