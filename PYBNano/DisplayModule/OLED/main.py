from machine import I2C
form pyb import ADC

i2c = (sda=Pin("PB9"),scl=Pin("PB8"))

from ssd1306 import SSD1306_I2C
oled = SSD1306_I2C(128,64,i2c)
t = ADCAll(12)
while True:
    te = t.read()
    oled.text(str(te),50,10)

