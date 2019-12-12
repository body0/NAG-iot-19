import common as Common
import eventLog as EventLog
import devEvent as DevEvent
import oledManager as OledManager

import sys
import time
import threading

import hashlib

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

ServiceFactory = None
class _ServiceFactory:

    def __init__(self):
            if(ServiceFactory != None):
                raise Exception('Triing to instanciate singleton')

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
            self._Buzer = (DevEvent.LED(-1), None)
            self._RedLed = (DevEvent.LED(-1), None)
            self._GreenLed = (DevEvent.LED(-1), None)

        def turnOnForFor(self, lightId, milis):
            if lightId == LightsIds.MAIN_HOUSE:
                pass
            elif lightId == LightsIds.ALARM_LED:
                self._turnOnLedFor(self._RedLed)
            elif lightId == LightsIds.ALARM_BUZZER:
                self._turnOnLedFor(self._Buzer)
            elif lightId == LightsIds.AUTH_SUCCES_LED:
                self._turnOnLedFor(self._GreenLed)
            else:
                self._Log.emit('lightId not found in LightsIds', EventLog.EventType.SYSTEM_WARN)
        
        def _turnOnLedFor(self, led):
            led[0].on()
            if led[1] != None:
                led[1].cancel()

            t = threading.Timer(milis, lambda : led[1].off())
            t.setDaemon(True)
            self.led[1] = t
            t.start()

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
            return hashlib.sha224(str.encode(string)).hexdigest()

        def _authFail():
            self._Lights.turnOnForFor(LightsIds.ALARM_BUZZER, 1000)
            self._Lights.turnOnForFor(LightsIds.ALARM_LED, 1000)
            self._Log.emit('AUTH FAIL', EventLog.EventType.WARN)

        def _authSucces()
            self._Lights.turnOnForFor(LightsIds.AUTH_SUCCES_LED, 1000)
            self._Log.emit('AUTH SUCCES', EventLog.EventType.LOG)
            
        
    class OledService:
        """
            ! SINGLETON !
        """
        def __init__(self):
            self._Log = EventLog.LogerService()
            self._Oled = OledManager.OLEDManager()
            self._Schema = [
                ("Light", "UNKNOWN"),
                ("Humidity": "UNKNOWN"),
                ("Temperature": "UNKNOWN"),
                ("GateState": "Down")
            ]
            self._Timer = None

             self._Oled.claer()
                for entry in self._Schema:
                    self._Oled.addLineCallback(lambda : entry[0] + ': ' + str(entry[1]))
        
        def setShemaEntry(self, name, text):
            for entry in self._Schema:
                if(entry[0] == name):
                    entry[1] = text
                    return True
            return False
        
        def showDiferentTextFor(self, textCallbackList, milis):
            if self._Timer != None:
                self._Timer.cancel()

            self._Oled.claer()
            for fun in textCallbackList:
                self._Oled.addLineCallback(fun)

            t = threading.Timer(milis, update)
            t.setDaemon(True)
            self._Timer = t
            t.start()

            def update():
                self._Oled.claer()
                for entry in self._Schema:
                    self._Oled.addLineCallback(lambda : entry[0] + ': ' + str(entry[1]))
                self._Timer = None

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
ServiceFactory = _ServiceFactory()

class AuthMethod:
    RFID = 0
    NUM = 1
    CAMERA = 2

class LightsIds:
    MAIN_HOUSE = 0
    ALARM_BUZZER = 1
    ALARM_LED = 2
    AUTH_SUCCES_LED = 3  

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