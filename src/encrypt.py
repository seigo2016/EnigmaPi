import random
from typing import List
import time
import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from util import lcd

alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l",
            "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]


class Enigma():
    def __init__(self, rotor: list, plug: list) -> None:
        self.plug = plug
        self.lcd = lcd.lcd()
        self.lcd.message = "Result"
        # self.lcd.cursor_position(0, 1)
        print(plug)
        self.key_list = [["Q", "W", "E", "R", "T", "Z", "U", "I", "O"],
                    ["A", "S", "D", "F", "G", "H", "J", "K", "enter"],
                    ["P", "Y", "X", "C", "V", "B", "N", "M", "L"]
                    ]

        i2c = busio.I2C(board.SCL, board.SDA)
        ads = ADS.ADS1015(i2c)
        self.channels = [None, None, None]
        self.channels[0] = AnalogIn(ads, ADS.P1)  # Q-O
        self.channels[1] = AnalogIn(ads, ADS.P0)  # A-K + enter
        self.channels[2] = AnalogIn(ads, ADS.P2)  # P-L
        self.scrumblers: List[List] = self.make_rotor(
            rotor[0], rotor[1], rotor[2], 0)
        self.scrumbler_1: List = self.scrumblers[0]
        self.scrumbler_2: List = self.scrumblers[1]
        self.scrumbler_3: List = self.scrumblers[2]
        self.replace_key()
        # シード,順序入力
        # seed1 = int(input("Scrumbler1のシード [default 0]>") or 0)
        # seed2 = int(input("Scrumbler2のシード [default 0]>") or 0)
        # seed3 = int(input("Scrumbler3のシード [default 0]>") or 0)

        # order = int(input("Scrumblerの順序 [default 0]>") or 0)

        # ローターの初期化
        # scrumblers:List[List] = make_rotor(seed1, seed2, seed3, order)

    def replace_key(self):
        #src_plug = []
        #dist_plug = []
        for p in self.plug:
            src_plug = p[0]["alphabet"].upper()
            dist_plug = p[1]["alphabet"].upper()
            src_i = -1
            dist_i = -1
            #src_plug.append(p[0]["alphabet"])
            #dist_plug.append(p[1]["alphabet"])
            for i, key_row in enumerate(self.key_list):
                try:
                    if key_row.index(src_plug):
                        #self.key_list[i][key_row.index(src_plug)] = dist_plug
                        src_i = key_row.index(src_plug)
                    if key_row.index(dist_plug):
                        #self.key_list[i][key_row.index(dist_plug)] = src_plug
                        dist_i = key_row.index(dist_plug)
                except ValueError:
                    pass
                print(src_i, dist_i)
                if src_i != -1:
                    self.key_list[i][src_i] = dist_plug
                if dist_i != -1:
                    self.key_list[i][dist_i] = src_plug
    def make_rotor(self, seed1=0, seed2=0, seed3=0, order=0) -> List[List]:
        scrumblers: List = [None, None, None]
        order_list = (
            (0, 1, 2),
            (0, 2, 1),
            (1, 0, 2),
            (1, 2, 0),
            (2, 0, 1),
            (2, 1, 0)
        )
        select_order = order_list[order]
        random.seed(seed1)
        scrumblers[select_order[0]] = random.sample(range(26), k=26)
        random.seed(seed2)
        scrumblers[select_order[1]] = random.sample(range(26), k=26)
        random.seed(seed3)
        scrumblers[select_order[2]] = random.sample(range(26), k=26)

        return scrumblers

    def detect_key(self, key) -> str:
        return self.key_list[key[0]][key[1]]
        # return key

    def detect_switch(self):
        # threshold:List[int] = [0, 2400, 5248, 8128, 11472, 14768, 18256, 21312, 24160, 26280]
        threshold: List[int] = [2300, 5148, 8028,
                                11372, 14668, 18156, 21212, 24060, 26180]
        key = (-1, -1)
        while True:
            # 入力をチェックする処理
            for chan_i, chan in enumerate(self.channels):
                value = chan.value
                for i, t in enumerate(threshold):
                    if t > value:
                        key = (chan_i, i)
                        break
                    else:
                        key = (-1, -1)
                if key[0] != -1:
                    time.sleep(0.3)
                    # print(key)
                    return self.detect_key(key)
            time.sleep(0.1)

    def encrypt(self) -> str:
        # ローターの回転位置
        roter_1_index = 0
        roter_2_index = 0
        roter_3_index = 0

        result_all: str = ""

        # 平文入力
        while True:
            plain_char = self.detect_switch()
            if plain_char == "enter":
                break
            print(plain_char)
#            print(plain_char)
            plain_index = alphabet.index(plain_char.lower())
            # 回転の反映
            now_scrumbler_1: List[int] = self.scrumbler_1[roter_1_index:] + \
                self.scrumbler_1[:roter_1_index]
            now_scrumbler_2: List[int] = self.scrumbler_2[roter_2_index:] + \
                self.scrumbler_2[:roter_2_index]
            now_scrumbler_3: List[int] = self.scrumbler_3[roter_3_index:] + \
                self.scrumbler_3[:roter_3_index]
            # ローター
            c1_index = now_scrumbler_1[plain_index]
            c2_index = now_scrumbler_2[c1_index]
            c3_index = now_scrumbler_3[c2_index]
            # リフレクター
            ref_index = (c3_index + 13) % 26
            r_c3_index = now_scrumbler_3.index(ref_index)
            r_c2_index = now_scrumbler_2.index(r_c3_index)
            r_c1_index = now_scrumbler_1.index(r_c2_index)

            # ローター1の回転
            roter_1_index += 1
            # ローター2の回転
            if roter_1_index == 25:
                roter_2_index += 1
            # ローター3の回転
            if roter_2_index == 25:
                roter_3_index += 1

            # 暗号文
            result_char: str = alphabet[r_c1_index]

            result_all += result_char

#            print(result_char)
            self.lcd.cursor_position(1, 0)
            self.lcd.cursor_position(0, 1+len(result_all))
            self.lcd.message=result_all
#            self.lcd.message="test"
        print("Finish")


if __name__ == '__main__':
    enigma = Enigma()
    enigma.encrypt()
