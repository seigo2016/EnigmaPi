from adafruit_mcp230xx.mcp23017 import MCP23017
import board
import busio
from digitalio import Direction
import json
import time
class EnigmaPlug:
    def __init__(self, address1=0x20, address2=0x21):
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.pin_pair = []
        self.mcp = [MCP23017(self.i2c, address=address1), MCP23017(self.i2c, address=address2)]
        self.get_pin_list()
        self.exist_pin = []
    def get_pin_list(self):
        with open('./plug_key_map.json') as f:
            d = json.load(f)
        plug_map = d["key"]
        self.plug_info = [{}]*26
        for i, plug in enumerate(plug_map):
            board_number = plug["board"]
            plug_mcp = self.mcp[board_number]
            pin_number = plug["side"] * 8 + plug["pin"]
#            print(pin_number)
            pin = plug_mcp.get_pin(pin_number)
            self.plug_info[i] = {"pin":pin, "alphabet":plug["key"]}
#            print()
#        print(self.plug_info)
    def get_pin_state(self):
        for i in range(26):
            src_plug = self.plug_info[i]
            src_plug['pin'].switch_to_output(value=True)
            for j in range(26):
                if i==j:
                    continue
                dst_plug = self.plug_info[j]
#                dst_plug['pin'].switch_to_output(value=False)
#                dst_plug['pin'].invert_polarity = True
                dst_plug['pin'].direction = Direction.INPUT
#                dst_plug['pin'].switch_to_input(value=False)
#                time.sleep(0.05)
#                print(dst_plug['pin'].value)
                if dst_plug['pin'].value and src_plug['alphabet'] not in self.exist_pin and dst_plug['alphabet'] not in self.exist_pin:
                    self.pin_pair.append((src_plug, dst_plug))
                    self.exist_pin.append(src_plug['alphabet'])
                    self.exist_pin.append(dst_plug['alphabet'])
            src_plug['pin'].switch_to_output(value=False)
            src_plug['pin'].direction = Direction.INPUT
        return self.pin_pair

if __name__ == '__main__':
    eng = EnigmaPlug()
    print(eng.get_pin_state())
