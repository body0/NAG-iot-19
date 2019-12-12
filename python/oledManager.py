from PIL import ImageFont
from PIL import ImageDraw
from PIL import Image
import time
import Adafruit_SSD1306
import threading
import sys

# import RPi.GPIO as GPIO
# GPIO.setmode(GPIO.BCM)


ERR_VERTICAL_OWERFLOW = "ERROR-WO"
ERR_HORIZONTAL_OWERFLOW = "ERROR-HO"


class OLEDManager:
    """
    OLEDManager Class
    takes list of text generating functions and displays their output in the display
    """
    def __init__(self, display, period):
        """
        :param display: Adafruit_SSD1306.SSD1306_128_64 object
        :param period: time betven automatic update of display content
        """
        self.Display = display  # Adafruit_SSD1306.SSD1306_128_64 object
        self.Fun = [lambda: ""]

        def update():
            self.draw()
            t = threading.Timer(period, update)
            t.setDaemon(True)
            t.start()

        update()

    def addLineCallback(self, callback):
        self.Fun.append(callback)
        
    def claer(self):
        self.Fun = []

    def draw(self):
        """
        :return:
        """
        width = self.Display.width
        height = self.Display.height
        image = Image.new('1', (width, height))
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype("/home/pi/Documents/test/oled/BebasNeue Regular.ttf",
                                  13)  # load custom font with size 13

        displayStr = []  # string displayed on the screen
        maxLength = 0  # max length of the longest line
        totalHeight = 10 * len(self.Fun)
        for i in range(len(self.Fun)):
            displayStr.append(str(self.Fun[i]()))
            size = draw.textsize(displayStr[i], font=font)
            maxLength = size[0] if (maxLength < size[0]) else maxLength

        if totalHeight == 0 or maxLength == 0:  # edge case, display empty screen
            displayStr = [" "]
            maxLength = 10
            totalHeight = 10

        if totalHeight > height - 3: # text too wide
            draw.text((1, 1), ERR_VERTICAL_OWERFLOW, font=font, fill=1)
        elif maxLength > width - 3:  # text too high
            draw.text((1, 1), ERR_HORIZONTAL_OWERFLOW, font=font, fill=1)
        else:
            draw.rectangle((0, 0, width - 1, height - 1), outline=1, fill=0)
            scale = min((height - 3) / totalHeight, (width - 3) / maxLength)
            newFont = ImageFont.truetype("/home/pi/Documents/test/oled/BebasNeue Regular.ttf",
                                         round(10 * scale))  # resize text
            rowHeight = draw.textsize("A", font=newFont)[1] + 2
            totalHeigth = rowHeight * len(displayStr) - 2
            space = (height - 2 - totalHeigth) / len(displayStr)

            for j in range(1, len(displayStr)):  # add line to image
                draw.line([(10, rowHeight * j + space * j), (width - 10, rowHeight * j + space * j)], fill=1, width=1)

            for j in range(len(displayStr)):  # add text to image
                preFixToMind = (width - draw.textsize(displayStr[j], font=newFont)[0]) / 2
                draw.text((preFixToMind, rowHeight * j + space * j + space / 2 + 1), displayStr[j], font=newFont, fill=1)
        self.Display.clear()
        self.Display.image(image)
        try:
            self.Display.display()
        except:
            print("ERR: display")
            sys.stdout.flush()


""" class SynchDisplay(Adafruit_SSD1306.SSD1306_128_64):
    def __init__(self):
        super(Adafruit_SSD1306.SSD1306_128_64, self).__init__(rst=24, width=128, height=64)
        self.writeLock = threading.Lock()

    def display(self):
        self.writeLock.acquire()
        super(SyncDisplay, self).display()
        self.writeLock.release()

    def image(self, image):
        try:
            self.writeLock.acquire()
            super(SyncDisplay, self).image(image)
            time.sleep(0.1)
            self.writeLock.release()
        except Exception as e:
            print("E: {}".format(e)) """


if __name__ == "__main__":
    disp = Adafruit_SSD1306.SSD1306_128_64(rst=24)
    disp.begin()
    oled = OLEDManager(disp, 0.5)
    oled.addFunc(lambda: "hello")
    oled.addFunc(lambda: "")
    oled.draw()

# testFun()