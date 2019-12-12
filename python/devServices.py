import common as Common
import eventLog as EventLog
import eventManager as EventManager
import oledManager as OledManager

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
class SlaveService:
    """
        ! SINGLETON !
        used to comunicate with arduino
    """
    def __init__(self):
        pass

class LightService:
    """
        ! SINGLETON !
        used to turn on and off 
    """
    def __init__(self):
        self._Log = EventLog.LogerService()

    def turnOnForFor(self, lightId, milis):
        pass

class LightsIds:
    MAIN_HOUSE = 0
    ALARM_BUZZER = 1
    ALARM_LED = 2
    AUTH_SUCCES_LED = 3  

class GateService:
    """
        ! SINGLETON !
        user can autentificate by rf-id, password or camera
        callback: (isOpened: boolealn) => void
    """
    def __init__(self, onGateStateChangeCallback):
        self._Log = EventLog.LogerService()
        self._OnGateStateChangeCallback = onGateStateChangeCallback
    
    def openFor(self, milis):
        pass

class AuthService:
    """
        ! SINGLETON !
        user can autentificate by rf-id, password or camera
        callback: (methond: AuthMethod) => void
    """
    def __init__(self, afterSuccesfullAuthCallback, afterFailedAuthCallback):
        self._Log = EventLog.LogerService()
        self._Lights = LightService()
        self.PasswordHash = '...'
        self.RfIdHash = '...'
        self._AfterSuccesfullAuthCallback = afterSuccesfullAuthCallback
        self._AfterFailedAuthCallback = afterFailedAuthCallback
    
    def _hash(self, string):
        return

    def _authFail():
        self._Lights.turnOnForFor(LightsIds.ALARM_BUZZER, 1000)
        self._Lights.turnOnForFor(LightsIds.ALARM_LED, 1000)
        self._Log.emit('AUTH FAIL', EventLog.EventType.WARN)

    def _authSucces()
        self._Lights.turnOnForFor(LightsIds.AUTH_SUCCES_LED, 1000)
        self._Log.emit('AUTH SUCCES', EventLog.EventType.LOG)
        
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
    
class OledService:
    """
        ! SINGLETON !
    """
    def __init__(self):
        self._Log = EventLog.LogerService()
        self._Oled = OledManager.OLEDManager()
        self._Schema = {

        }
    
    def setShemaEntry(self, name, text):
        pass
    
    def showDiferentTextFor(self, text, milis):
        pass

class CameraService:
    """
        ! SINGLETON !
    """
    def __init__(self):
        self._Log = EventLog.LogerService()
    
    def getPic():
        pass

    def auth():
        pass