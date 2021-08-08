import board
import busio
import adafruit_character_lcd.character_lcd as characterlcd
from adafruit_mcp230xx.mcp23017 import MCP23017
import time

def lcd(address=0x23):

    lcd_columns = 16
    lcd_rows = 2

    i2c = busio.I2C(board.SCL, board.SDA)
    mcp = MCP23017(i2c, address=address)

    lcd_rs = mcp.get_pin(0)
    lcd_en = mcp.get_pin(1)
    lcd_d4 = mcp.get_pin(2)
    lcd_d5 = mcp.get_pin(3)
    lcd_d6 = mcp.get_pin(4)
    lcd_d7 = mcp.get_pin(5)
    lcd_a = characterlcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
                                          lcd_columns, lcd_rows)

    return lcd_a

