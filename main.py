import time
import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

i2c = busio.I2C(board.SCL, board.SDA)

ads = ADS.ADS1015(i2c)
channels = [None]
channels[0] = AnalogIn(ads, ADS.P0)

while True:
    print(channels[0].voltage, channels[0].value)
    time.sleep(1)
