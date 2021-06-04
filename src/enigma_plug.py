from adafruit_mcp230xx.mcp23017 import MCP23017
import board
import busio
from digitalio import Direction

class EnigmaPlug:
    def __init__(self):
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.pin_pair = []
        mcp = MCP23017(self.i2c)
        self.pin_all = []
        for i in range(8):
            pin = mcp.get_pin(i)
            self.pin_all.append(pin)

    def get_pin_state(self):
        for i in range(8):
            src_pin = self.pin_all[i]
            # src_pin.switch_to_output(value=True)
            src_pin.direction = Direction.OUTPUT
            src_pin.value=True
            for j in range(8):
                if i==j:
                    continue
                # self.pin_all[j].switch_to_output(value=False)
                self.pin_all[j].direction = Direction.INPUT
                self.pin_all[j].value = False
                if self.pin_all[j].value:
                    self.pin_pair.append((i, j))
            # src_pin.switch_to_output(value=False)
            src_pin.direction = Direction.INPUT
            src_pin.value=False
        return self.pin_pair