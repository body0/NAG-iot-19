import common as Common

""" 
    COMPLEX EXTERNAL DEVICE

        - GateServices
        - AuthServices
        - Oled (wraper)
        - Camera (wraper)
        - SensorTimer (base class for each sensor, that needs to be periodicly updated)
"""

class AuthServices:

    def getUsed():
        return 
        
class AuthMethod:
    RFID = 0
    NUM = 1
    CAMERA = 2

class SensorTimer:
    def __init__(self, loadNewValCallback):
        self._InterObs = Common.MemObservable()
        self._LoadNewValCallback = loadNewValCallback

    def subscribe(self, callback):
        return

        """
        start periodicly calling init callback in new thread
        :param period:  update value every 'perion' second
    """
    def start(self, period):
        def update():
            newVal = self._LoadNewValCallback()
            t = threading.Timer(period, update)
            t.setDaemon(True)
            t.start()

        if self.TimerStarted:
            return
        update()

    def stopAndClean(self):
        pass
    