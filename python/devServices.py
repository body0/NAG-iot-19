import common as Common
import eventLog as EventLog
import eventManager as EventManager

import sys
import time
import threading

""" 
    COMPLEX EXTERNAL DEVICE
        
        - Define higher-level senzor information and pin numbers
        - Do not define data flow betwen service and upstream 
        - Classes
            - GateService (service)
            - AuthService (service)
            - SlaveSrvice (service)
            - Oled (wraper)
            - Camera (wraper)
            - SensorTimer (base class for each sensor, that needs to be periodicly updated)
"""
class SlaveSrvice:
    """
        ! SINGLETON !
        used to comunicate with arduino
    """
    def __init__(self):
        pass

class GateService:
    """
        ! SINGLETON !
        user can autentificate by rf-id, password or camera
        callback: (methond: AuthMethod) => void
    """
    def __init__(self, onGateStateChangeCallback):
        self._OnGateStateChangeCallback = onGateStateChangeCallback


class AuthService:
    """
        ! SINGLETON !
        user can autentificate by rf-id, password or camera
        callback: (methond: AuthMethod) => void
    """
    def __init__(self, afterSuccesfullAuthCallback, afterFailedAuthCallback):
        # self._AuthMode = AuthMethod
        self.PasswordHash = '...'
        self.RfIdHash = '...'
        self._AfterSuccesfullAuthCallback = afterSuccesfullAuthCallback
        self._AfterFailedAuthCallback = afterFailedAuthCallback
    
    def _hash(self, string):
        return
        
class AuthMethod:
    RFID = 0
    NUM = 1
    CAMERA = 2

class SensorTimer:
    def __init__(self, loadNewValCallback):
        self._InterObs = Common.MemObservable()
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

    def stopAndClean(self):
        self._Timer.cancel()
        self._Timer == None
        self._InterObs = Common.MemObservable()
        pass
    