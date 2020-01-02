import threading
from enum import Enum

""" 
====== ENUM ======
"""

class AuthMethod(Enum):
    RFID = 0
    NUM = 1
    CAMERA = 2

class LightsIds(Enum):
    MAIN_HOUSE = 'House Lights'
    ALARM_BUZZER = 'Alarn'
    ALARM_LED = 'Alarm Led'
    AUTH_SUCCES_LED = 'Green Led'

class LedState(Enum):
    OFF = 'OFF'
    ON = 'ON'
    OSCILATING = 'BLINKING'

class InputIds(Enum):
    LIGTHS_BUTTON = 0
    GATE_BUTTON = 1
    NUM_PAD = 2


""" 
====== CLASSES ======
"""

class Observable:
    """
        call 'callback' when emit is called
        callback: (data: any) => () => void
                - returs destructor for this substription
    """
    def __init__(self):
        self._Subscriptions = {}
        self._LastKey = 0

    def subscrie(self, callback):
        key = str(self._LastKey)
        self._Subscriptions[key] = callback
        self._LastKey += 1
        def destructor():
            del self._Subscriptions[key]
        return destructor
    
    def emit(self, data):
        for callbackName in self._Subscriptions:
            self._Subscriptions[callbackName](data)

class MemObservable(Observable):
    """
        call 'callback' when emit is called
        callback: (data: any) => () => void
                - returs destructor for this substription
    """
    def __init__(self):
        self._LastValue = None

    def emit(self, data):
        self._LastValue = None
        super().emit(data)
        
    def getLast(self):
        return self._LastValue

class Timeout:
    def __init__(self, calback, milis):
        t = threading.Timer(milis, calback)
        self._Timer = t
        t.setDaemon(True)
        t.start()

    def cansel(self):
        self._Timer.cancel()

class SensorTimer:
    def __init__(self, loadNewValCallback):
        self._InterObs = MemObservable()
        self._LoadNewValCallback = loadNewValCallback
        self._Timer = None

    def subscribe(self, callback):
        self._InterObs.subscrie(callback)

    """
        start periodicly calling init callback in new thread
        :param period:  update value every 'perion' second
    """
    def start(self, period):
        def update():
            newVal = self._LoadNewValCallback()
            self._InterObs.emit(newVal)
            t = threading.Timer(period, update)
            t.setDaemon(True)
            self._Timer = t
            t.start()

        if self._Timer == None:
            return
        update()

    def stopAndClearAllSubscriptions(self):
        self._Timer.cancel()
        self._Timer == None
        self._InterObs = MemObservable()
        pass