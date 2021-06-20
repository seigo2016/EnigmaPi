from adafruit_mcp230xx.mcp23017 import MCP23017
import board
import busio
from digitalio import Direction
import json

class EnigmaPlug:
    def __init__(self, address1=0x20, address2=0x21):
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.pin_pair = []
        self.mcp = [MCP23017(self.i2c, address=address1), MCP23017(self.i2c, address=address2)]
        self.get_pin_list()

    def get_pin_list(self):
        with open('../plug_key_map.json') as f:
            d = json.load(f)
        plug_map = d["key"]
        plug_info = [{}]*26
        for i, plug in enumerate(plug_map):
            board_number = plug["board"]
            plug_mcp = self.mcp[board_number]
            pin_number = plug["side"] * 8 + plug["pin"]
            pin = plug_mcp.get_pin(pin_number)
            plug_info[i] = {"pin":pin, "alphabet":plug["key"]}

    def get_pin_state(self):
        for i in range(8):
            src_plug = self.plug_info[i]
            src_plug[0].switch_to_output(value=True)
            for j in range(8):
                if i==j:
                    continue
                dst_plug = self.plug_info[j]
                dst_plug[0].direction = Direction.INPUT
                if dst_plug[0].value:
                    self.pin_pair.append((src_plug, dst_plug))
            src_plug[0].switch_to_output(value=False)
            src_plug[0].direction = Direction.INPUT
        return self.pin_pair

eng = EnigmaPlug()
print(eng.get_pin_state())