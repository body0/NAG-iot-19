import smbus

def getSlaveService():
    return SlaveService

class _SlaveService:
    """
        ! SINGLETON !
        used to comunicate with arduino
    """

    def __init__(self):
        self.adress = 0xAA
        #self.bus = smbus.SMBus(0)

    def ledOn(self, led=0):
        if led < 16:
            self.bus.write_byte(self.adress, SlaveCommands.LED_ON | led)
        else:
            raise Exception("Leds : Invalid number!")

    def ledOff(self, led=0):
        if led < 16:
            self.bus.write_byte(self.adress, SlaveCommands.LED_OFF | led)
        else:
            raise Exception("Leds : Invalid number!")

    def openGate(self):
        self.setGate(True)

    def closeGate(self):
        self.setGate(False)

    def setGate(self, position = True):
        if position:
            self.bus.write_byte(self.adress, SlaveCommands.GATE | 0x0F)
        else:
            self.bus.write_byte(self.adress, SlaveCommands.GATE)

class SlaveCommands:
    LED_ON = 0x10
    LED_OFF = 0x20
    GATE = 0x30

SlaveService = _SlaveService()