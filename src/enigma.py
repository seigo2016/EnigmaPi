import random
import itertools
from typing import List
import readchar
import time
import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn


alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

i2c = busio.I2C(board.SCL, board.SDA)

ads = ADS.ADS1015(i2c)

channels = [None, None, None]
channels = [None, None]
channels[0] = AnalogIn(ads, ADS.P0) # A-K + enter
channels[1] = AnalogIn(ads, ADS.P1) # Q-O
#channels[2] = AnalogIn(ads, ADS.P2) # P-L

def make_rotor(seed1=0, seed2=0, seed3=0, order=0) -> List[List]:
    scrumblers:List = [None,None,None]
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

def detect_key(chan_i, key) -> str:
    key_list = [["Q", "W", "E", "R", "T", "Z", "U", "I", "O"],
                ["A", "S", "D", "F", "G", "H", "J", "K", "enter"],
                ["P", "Y", "X", "C", "V", "B", "N", "M", "L"]
                ]
    print(key_list[chan_i][key])
    return key

def detect_switch():
    # threshold:List[int] = [0, 2400, 5248, 8128, 11472, 14768, 18256, 21312, 24160, 26280]
    threshold:List[int] = [2300, 5148, 8028, 11372, 14668, 18156, 21212, 24060, 26180]
    key = (-1, -1)
    while True:
        ### 電圧入力をチェックする処理
        for chan_i, chan in enumerate(channels):
#            print(chan_i, chan.value)
            value = chan.value
            prev_key = key
            #print(prev_key)
            for i, t in enumerate(threshold):
                if t > value:
                    key = (chan_i, i)
                    break
                else:
                    key = (-1, -1)
#            if prev_key[1] != -1 and key == prev_key:
            if key[0] != -1:
                time.sleep(0.3)
                return detect_key(chan_i, key[1])
        time.sleep(0.1)


def main() -> str:
    # シード,順序入力
    # seed1 = int(input("Scrumbler1のシード [default 0]>") or 0)
    # seed2 = int(input("Scrumbler2のシード [default 0]>") or 0)
    # seed3 = int(input("Scrumbler3のシード [default 0]>") or 0)

    # order = int(input("Scrumblerの順序 [default 0]>") or 0)

    # ローターの初期化
    # scrumblers:List[List] = make_rotor(seed1, seed2, seed3, order)
    scrumblers:List[List] = make_rotor(0, 0, 0, 0)
    scrumbler_1:List = scrumblers[0]
    scrumbler_2:List = scrumblers[1]
    scrumbler_3:List = scrumblers[2]

    # ローターの回転位置
    roter_1_index = 0
    roter_2_index = 0
    roter_3_index = 0

    result_all:str =""

    # 平文入力
    while True:
        # plain_text:str = input(">")
        # plain_char:str = readchar.readkey()

        # plain_char = plain_char.lower()

        plain_char = detect_switch()
        #print(plain_char)
        continue
        plain_index = alphabet.index(plain_char)
        # 回転の反映
        now_scrumbler_1:List[int] = scrumbler_1[roter_1_index:] + scrumbler_1[:roter_1_index]
        now_scrumbler_2:List[int] = scrumbler_2[roter_2_index:] + scrumbler_2[:roter_2_index]
        now_scrumbler_3:List[int] = scrumbler_3[roter_3_index:] + scrumbler_3[:roter_3_index]
        # ローター
        c1_index = now_scrumbler_1[plain_index]
        c2_index = now_scrumbler_2[c1_index]
        c3_index = now_scrumbler_3[c2_index]
        # リフレクター
        ref_index = (c3_index + 13)%26
        r_c3_index = now_scrumbler_3.index(ref_index)
        r_c2_index = now_scrumbler_2.index(r_c3_index)
        r_c1_index = now_scrumbler_1.index(r_c2_index)

        #ローター1の回転
        roter_1_index += 1
        #ローター2の回転
        if roter_1_index == 25:
            roter_2_index += 1
        #ローター3の回転
        if roter_2_index == 25:
            roter_3_index += 1
        
        #暗号文
        result_char:str = alphabet[r_c1_index]

        result_all += result_char

        print(result_char)
        print(result_all)

print(main())
