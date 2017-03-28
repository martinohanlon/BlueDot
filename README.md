
# Blue Dot

BlueDot is a bluetooth remote and zero boiler plate (super simple to use :) python library for the Raspberry Pi. 

You can use the Blue Dot app to control your raspberry pi wirelessly using Bluetooth.

## Current Status

Alpha - it works, but expect rough edges and future changes which break compatability.

## Installation

### Blue Dot client

The Blue Dot app is available from the Android Play Store - tbc.

### Python library

Open a terminal, click `Menu > Accessories > Terminal`:

```
sudo pip3 install bluedot
```

## Usage

### Pairing

In order to connect the Blue Dot app you will need to pair the client (android phone) to the Raspberry Pi.

[instructions to go here]

### Python program

1. Start up Python 3, click `Menu > Programming > Python 3`
2. Click `File > New File` to create a new program
3. Create your python program:

```python
from bluedot import BlueDot
dot = BlueDot()
dot.wait_for_press()
print("You pressed the blue dot!")
```

4. Run the program, click `Run > Run Module` or press `F5`

### Blue Dot App

Start the BlueDot app, connect to your Raspberry Pi, press the blue dot. 

## Documentation

Will be online soon!  Until then, check out the inline documentation in the code :)