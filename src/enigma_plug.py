import pigpio
import time
from  adafruit_mcp230xx.mcp23017 import MCP23017
import board
import busio
from digitalio import Direction, Pull

i2c = busio.I2C(board.SCL, board.SDA)
mcp = MCP23017(i2c)
pin_all = []
for i in range(8): # GPIOA (片側8ピンのみテスト中)
    pin = mcp.get_pin(i)
    pin_all.append(pin)

for i in range(8):
    src_pin = pin_all[i]
    src_pin.switch_to_output(value=True)
    src_pin.direction = Direction.OUTPUT
    src_pin.value=True
    for j in range(8):
        if i==j:
            continue
        pin_all[j].switch_to_output(value=False)
        pin_all[j].direction = Direction.INPUT
        pin_all[j].value = False
        if pin_all[j].value:
            print(i, j)
    src_pin.switch_to_output(value=False)
    src_pin.direction = Direction.INPUT
    src_pin.value=False
