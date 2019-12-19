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
        self._Subscriptions[] = callback
        self._LastKey += 1
        return lambda : del self._Subscriptions[key]
    
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