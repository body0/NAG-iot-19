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