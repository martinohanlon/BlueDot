import pytest
from bluedot.btcomm import BluetoothAdapter

try:
    bta = BluetoothAdapter("hci0")
except Exception as e:
    if str(e) == "Bluetooth adapter hci0 not found":
        pytest.skip("Bluetooth adapter hci0 not found - skipping test", allow_module_level = True)

def test_bluetooth_adapter():
    bta = BluetoothAdapter()
    assert bta.device == "hci0"
    assert len(bta.address) == 17

    # get the initial state of the adapter
    powered = bta.powered
    discoverable = bta.discoverable
    pairable = bta.pairable

    # flip the values back and forward
    bta.powered = not powered
    assert bta.powered == (not powered)
    bta.powered = powered
    assert bta.powered == powered

    # power up the adapter so discoverable and pairable can be tested
    bta.powered = True
    assert bta.powered == True

    bta.discoverable = not discoverable
    assert bta.discoverable == (not discoverable)
    bta.discoverable = discoverable
    assert bta.discoverable == discoverable

    bta.pairable = not pairable
    assert bta.pairable == (not pairable)
    bta.pairable = pairable
    assert bta.pairable == pairable

    bta.allow_pairing()
    assert bta.pairable == True
    assert bta.discoverable == True

    # reset the adapter back
    bta.powered = powered
    bta.discoverable = discoverable
    bta.pairable = pairable