import threading
""" 
    COMMON PYTHON CONSTRUCTION
        - observable
"""

class Observable:
    """
        call 'callback' when emit is called
        callback: (data: any) => () => void
                - returs destructor for this substription
    """
    def __init__(self):
        self._Subscriptions = {}
        self._LastKey = 0;

    def subscrie(self, callback):
        key = str(self._LastKey)
        self._Subscriptions[key] = callback
        self._LastKey += 1
        def destructor():
            del self._Subscriptions[key]
        return destructor
    
    def emit(self, data):
        for callback in self._Subscriptions:
            callback(data)

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