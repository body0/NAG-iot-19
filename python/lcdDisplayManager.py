import lib.lcddriver as LcdDisplayLib
import threading
import time


class LcdDisplay:
    """
        - manage Lcd higher function like: 
            - periodicly write to display new data
            - split text to multiple lines
            - cycle throught multiple pagees of lines if all lines cannot be displayed simultaneously
        warn: word cannot be longer than 20 characters
    """
    def __init__(self):
        self.Lcd = LcdDisplayLib.lcd()
        self.Lcd.lcd_clear()
        self.Cycle = []
        self.OverideMsg = False
        self._Timer = None
        self._OfsetCount = 0 # thread acces only

    """
        param func: func() => string
        - Add function that will return data that will be displayed on one or more lines (It will start at new line).
        - All functions added this way will be called when display is redrawn.
    """
    def addCycleLine(self, func):
        self.Cycle.append(func)

    def clearCycleLine(self):
        self.Cycle = []

    """
        - insted of isplayng data from "Cycle"  display "msg" insted
    """
    def setOverwriteMsg(self, msg):
        if len(msg) > 20:
            return
        self.OverideMsg = msg
        self.draw()

    def clearOverwriteMsg(self):
        self.OverideMsg = None
        self.draw()

    """
        - draw to display 
            - if OverideMsg is set display it in one line
            - else generate and slit text from all functions
    """
    def draw(self):
        """
            - splite only betwen words
            - for larger text inefficient algoritm for spliting: O(N^2)
        """
        def splitToLines(msg):
            MAX_LINE = 20
            arr = []
            words = msg.split(' ')
            line = ''
            for word in words:
                if len(word) > MAX_LINE:
                    return ['ERR: MAX SIZE'] # display err msg
                elif len(line) + len(word) > MAX_LINE:
                    arr.append(line)
                    line = word + ' '
                else:
                    line = line + word + ' '
            arr.append(line)
            return arr

        def writeLine(line, msg):
            self.Lcd.lcd_display_string(msg, line + 1)

        # display text to right line
        def printAll(arrToPrint):
            self.Lcd.lcd_clear()
            for i in range(len(arrToPrint)):
                msg = arrToPrint[i]
                writeLine(i, msg)

        # stop page changing
        if self._Timer != None:
            self._Timer.cancel()

        if self.OverideMsg:
            self.Lcd.lcd_clear()
            writeLine(1, self.OverideMsg)
        else:
            def moveLine():
                UPDATE_PERIOD = 5
                DISPLAY_HEIGHT = 4
                arr = []
                for fun in self.Cycle:
                    arr = arr + splitToLines(fun())
                if len(arr) > DISPLAY_HEIGHT:
                    toPrintArr = arr[self._OfsetCount: self._OfsetCount + DISPLAY_HEIGHT]
                    printAll(toPrintArr)
                    self._OfsetCount += DISPLAY_HEIGHT
                    # end of cycle
                    if self._OfsetCount >= len(arr):
                        self._OfsetCount = 0
                else:
                    printAll(arr)
                    
                t = threading.Timer(UPDATE_PERIOD, moveLine)
                self._Timer = t
                t.setDaemon(True)
                t.start()
            moveLine()
           
# debug
if __name__ == "__main__":
    display = LcdDisplay()
    display.addCycleLine(lambda: 'Hallo 1')
    display.addCycleLine(lambda: 'Hallo 2')
    display.addCycleLine(lambda: 'Hallo 3')
    display.addCycleLine(lambda: 'Hallo 4')
    display.addCycleLine(lambda: 'Hallo 5')
    display.draw()
    while True:
        time.sleep(100)
