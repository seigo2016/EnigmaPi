import pigpio
import time
from  adafruit_mcp230xx.mcp23017 import MCP23017
import board
import busio
from digitalio import Direction, Pull

i2c = busio.I2C(board.SCL, board.SDA)
mcp = MCP23017(i2c)
#pin2 = mcp.get_pin(2)
#pin6 = mcp.get_pin(6)
#pin6.switch_to_output(value=False)
#pin2.direction = Direction.OUTPUT
#pin6.direction = Direction.INPUT
#pin6.value= False
#pin2.value = True
pin_all = []
#print(pin6.value)
for i in range(8):
    pin = mcp.get_pin(i)
    pin_all.append(pin)

for i in range(8):
    pin = pin_all[i]
    pin.switch_to_output(value=True)
    pin.direction = Direction.OUTPUT
    pin.value=True
    for j in range(8):
        if i==j:
            continue
        pin_all[j].switch_to_output(value=False)
        pin_all[j].direction = Direction.INPUT
        pin_all[j].value = False
        if pin_all[j].value:
            print(i, j)
    pin.switch_to_output(value=False)
    pin.direction = Direction.INPUT
    pin.value=False

