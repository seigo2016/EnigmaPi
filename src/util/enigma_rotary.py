from adafruit_mcp230xx.mcp23017 import MCP23017
import board
import busio
from digitalio import Direction

class EnigmaRotary():
    def __init__(self, address=0x22):
        i2c = busio.I2C(board.SCL, board.SDA)
        self.mcp = MCP23017(i2c, address=address)
        self.rotaly_switch = [[None] * 5 for i in range(3)]
        self.selected_switch = [None, None, None]

        for i in range(3):
            for j in range(5):
                pin = self.mcp.get_pin(i*5+j)
#                print(i*5+j)
                self.rotaly_switch[i][j] = pin
                pin.direction = Direction.INPUT
                pin.value = False

    def get_state(self):
        for switch_i, switch in enumerate(self.rotaly_switch):
            for position_i, position_key in enumerate(switch):
                if position_key.value:
                    print(position_key.value)
                    self.selected_switch[switch_i] = position_i
                    break

        return self.selected_switch

if __name__ == '__main__':
    eng = EnigmaRotary()
    print(eng.get_state())
