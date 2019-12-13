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
    def subscrie(self, callback):
        return
    
    def emit(self, data):
        pass

class MemObservable(Observable):
    """
        call 'callback' when emit is called
        callback: (data: any) => () => void
                - returs destructor for this substription
    """
    def subscrie(self, callback):
        return
    
    def emit(self, data):
        pass

    def getLast(self):
        return

class Timeout:
    def __init__(self, calback, milis):
        t = threading.Timer(milis, calback)
        self._Timer = t
        t.setDaemon(True)
        t.start()

    def cansel(self):
        self._Timer.cancel()