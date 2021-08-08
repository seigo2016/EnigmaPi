import readchar
import check_status
import encrypt
from util import enigma_rotary, enigma_plug, lcd
import time
import sys


def start():
    try:
        lcd_a = lcd.lcd()
        while True:
            # message = "Please enter any key to configure"
            # lcd_a.message = message
            _ = readchar.readkey()
            lcd_a.clear()
            lcd_a.message = "Start"
            time.sleep(3)
            # GPIO(トグルスイッチ読み取り)
            lcd_a.clear()
            # ステータスチェック
            lcd_a.message = "Config Check"
            time.sleep(1.5)
            try:
                check_status.check()
            except check_status.I2CDeviceNotFoundError as e:  # 問題があればLCDに表示して再チェックを待つ
                lcd_a.message = str(e)
                continue

            # モード切替を待つ
    #        print("Please enter any key to change the mode")
    #        _ = readchar.readkey()
    #        print("")
            lcd_a.clear()
            lcd_a.message = "Config Check OK"
            lcd_a.cursor_position(0, 1)
            lcd_a.message = "Enigma Init"
            rotary = enigma_rotary.EnigmaRotary()
            rotary_state = rotary.get_state()
    #        lcd_a.cursor_position(11, 1)
    #        lcd_a.message = "."
            plug = enigma_plug.EnigmaPlug()
            plug_state = plug.get_pin_state()
    #        lcd_a.cursor_position(12, 1)
    #        lcd_a.message = "."
    #        enigma = encrypt.Enigma(rotary_state, plug_state)
    #        lcd_a.cursor_position(13, 1)
    #        lcd_a.message = "."
            lcd_a.cursor_position(0, 1)
            lcd_a.message = "Enigma Init OK"
            time.sleep(3)
            enigma = encrypt.Enigma(rotary_state, plug_state)
            lcd_a.clear()
            lcd_a.message = "Result"
            enigma.encrypt()
    except KeyboardInterrupt:
        print("Finished")
        sys.exit(0)


if __name__ == '__main__':
    start()

