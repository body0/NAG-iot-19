import lib.lcddriver as LcdDisplayLib
import threading
import time


class LcdDisplay:

    def __init__(self):
        self.Lcd = LcdDisplayLib.lcd()
        self.Lcd.lcd_clear()
        self.Cycle = []
        self.OverideMsg = False
        self._Timer = None
        self._OfsetCount = 0 # thread acces only

    def addCycleLine(self, func):
        self.Cycle.append(func)

    def overwriteMsg(self, msg):
        self.OverideMsg = msg
        self.draw()

    def draw(self):
        def splitToLines(msg):
            MAX_LINE = 20
            arr = []
            words = msg.split(' ')
            line = ''
            for word in words:
                if len(word) > MAX_LINE:
                    return ['ERR: MAX SIZE']
                elif len(line) + len(word) > MAX_LINE:
                    arr.append(line)
                    line = word + ' '
                else:
                    line = line + word + ' '
            arr.append(line)
            return arr

        def writeLine(line, msg):
            self.Lcd.lcd_display_string(msg, line + 1)

        def printAll(arrToPrint):
            self.Lcd.lcd_clear()
            for i in range(len(arrToPrint)):
                msg = arrToPrint[i]
                writeLine(i, msg)

        if self._Timer != None:
            self._Timer.cancel()

        if self.OverideMsg:
            self.Lcd.lcd_clear()
            writeLine(1, self.OverideMsg)
        else:
            def moveLine():
                arr = []
                for fun in self.Cycle:
                    arr = arr + splitToLines(fun())
                if len(arr) > 4:
                    toPrintArr = arr[self._OfsetCount: self._OfsetCount + 4]
                    """ for i in range(4):
                        line = arr[(self._OfsetCount + i) % len(arr)]
                        toPrintArr.append(line) """
                    printAll(toPrintArr)
                    #print('NEXT', self._OfsetCount, len(arr))
                    self._OfsetCount += 4
                    #self._OfsetCount %= len(arr)
                    if self._OfsetCount >= len(arr):
                        self._OfsetCount = 0
                else:
                    printAll(arr)
                    
                t = threading.Timer(5, moveLine)
                self._Timer = t
                t.setDaemon(True)
                t.start()
            print('timer start')
            moveLine()
           

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
