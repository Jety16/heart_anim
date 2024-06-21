from machine import Pin, SPI, I2C
from ssd1306 import SSD1306_I2C
import time


class DISPLAY():
    def __init__(self):
        self.hspi = SPI(1)  # sck=14 (scl), mosi=13 (sda), miso=12 (unused)
        self.i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
        self.oled = SSD1306_I2C(128, 64, self.i2c)

    def _draw_heart(self, x, y, size, filled):
        # Define the heart shape in a grid
        heart_shape = [
            " 0110 0110 ",
            "1111111111",
            "1111111111",
            " 11111111 ",
            "  111111  ",
            "   1111   ",
            "    11    ",
        ]

        for row in range(len(heart_shape)):
            for col in range(len(heart_shape[row])):
                if heart_shape[row][col] == "1":
                    if filled:
                        self.oled.fill_rect(x + col*size, y + row*size, size, size, 1)
                    else:
                        self.oled.rect(x + col*size, y + row*size, size, size, 1)

    def anim_heart(self):
        x = 40
        y = 20
        size = 2
        steps = 5
        while True:
            for i in range(steps):
                self.oled.fill(0)
                self._draw_heart(x, y, size + i, filled=True)
                self.oled.show()
                time.sleep(0.1)

            for i in range(steps):
                self.oled.fill(0)
                self._draw_heart(x, y, size + steps - i - 1, filled=False)
                self.oled.show()
                time.sleep(0.1)

    def _load(self, load_cycles):
        for i in range(load_cycles):
            for j in range(0, 70):
                self.oled.hline(30, 30, j, 1)
                self.oled.show()

            for j in range(30, 100):
                self.oled.pixel(j, 30, 0)
                self.oled.show()
            time.sleep(0.05)


display = DISPLAY()
display._load(1)
switch = Pin(10, Pin.IN)
while True:
    if switch.value():
        display.anim_heart()

