import common as Common
import eventLog as EventLog
import devEvent as DevEvent
import slaveService as SlaveService
import settingsService as SettingsService
#import oledManager as OledManager
import camera as Camera

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


""" 
    ===== SERVICES =====
"""

def getUserInputs():
    return UserInputs

class _UserInputs:
    def __init__(self):
        self._LightsButton = DevEvent.Button(14)
        self._GateButton = DevEvent.Button(15)
        self._Log = EventLog.getLoginServise()
        # self._numPad = DevEvent.NumBoard([-1, -1, -1], [-])

        """ def _generateInputButtonTuple(pinID):
            button =  DevEvent.Button(pinID)
            observable = Common.Observable()
            button.subscribe(lambda data: observable.emit(data))
            return (button, observable) """

    def subscribe(self, inputId, callback):
        if inputId == Common.InputIds.LIGTHS_BUTTON:
            self._LightsButton.subscribe(callback)
        elif inputId == Common.InputIds.GATE_BUTTON:
            self._GateButton.subscribe(callback)
        elif inputId == Common.InputIds.NUM_PAD:
            pass
        else:
            self._Log.emit('lightId not found in LightsIds', EventLog.EventType.SYSTEM_WARN)

def getLightService():
    return LightService
class _LightService:
    """
        ! SINGLETON !
        used to turn on and off
    """
    def __init__(self):
        self._Log = EventLog.getLoginServise()

        self._Buzer = [DevEvent.LED(10), None, Common.LedState.OFF]
        self._RedLed = [DevEvent.LED(11), None, Common.LedState.OFF]
        self._GreenLed = [DevEvent.LED(12), None, Common.LedState.OFF]
        #self._WhiteLed = [DevEvent.LED(-1), None, LedState.OFF]

    def turnOnLedFor(self, lightId, milis):

        def _turnOnLedFor(led):
            if led[1] != None:
                led[1].cancel()
            led[0].on()
            led[2] = Common.LedState.ON

            def afterLedOff():
                led[1].off()
                led[2] = Common.LedState.OFF
                self._Log.emit('Light state change', EventLog.EventType.LOG, {
                    'name': lightId,
                    'state': False
                })

            t = threading.Timer(milis /1000, afterLedOff)
            t.setDaemon(True)
            led[1] = t  
            self._Log.emit('Light state change', EventLog.EventType.LOG, {
                'name': lightId,
                'state': True
            })
            t.start()

        if lightId == Common.LightsIds.MAIN_HOUSE:
            pass
        elif lightId == Common.LightsIds.ALARM_LED:
            _turnOnLedFor(self._RedLed)
        elif lightId == Common.LightsIds.ALARM_BUZZER:
            _turnOnLedFor(self._Buzer)
        elif lightId == Common.LightsIds.AUTH_SUCCES_LED:
            _turnOnLedFor(self._GreenLed)
        else:
            self._Log.emit('lightId not found in LightsIds', EventLog.EventType.SYSTEM_WARN)

    def turnOnForFor(self, lightId, milis, period=1000, rounds=5):
        def _oscilateFor(led):
            def generateUpdate(roundsRemaining, newState):
                def update():
                    if roundsRemaining <= 0:
                        led[0].off()
                        led[2] = Common.LedState.OFF
                        self._Log.emit('Light state change', EventLog.EventType.LOG, pld={
                            'name': lightId,
                            'state': False
                        })
                    else:
                        if(newState):
                            led[0].on()
                        else:
                            led[0].off()
                        t = threading.Timer(period, generateUpdate(roundsRemaining - 1, not newState))
                        t.setDaemon(True)
                        led[1] = t
                        t.start()
                return update
            if led[1] != None:
                led[1].cancel()
            led[0].on()
            led[2] = Common.LedState.OSCILATING
            self._Log.emit('Light state change', EventLog.EventType.LOG, pld={
                'name': lightId,
                'state': True
            })
            t = threading.Timer(period, generateUpdate(rounds * 2, False))
            t.setDaemon(True)
            t.start()
        
        if lightId == Common.LightsIds.MAIN_HOUSE:
            pass
        elif lightId == Common.LightsIds.ALARM_LED:
            _oscilateFor(self._RedLed)
        elif lightId == Common.LightsIds.ALARM_BUZZER:
            _oscilateFor(self._Buzer)
        elif lightId == Common.LightsIds.AUTH_SUCCES_LED:
            _oscilateFor(self._GreenLed)
        else:
            self._Log.emit('lightId not found in LightsIds', EventLog.EventType.SYSTEM_WARN)

    def getLedState(self, lightId):
        if lightId == Common.LightsIds.MAIN_HOUSE:
            pass
        elif lightId == Common.LightsIds.ALARM_LED:
            return self._RedLed[2]
        elif lightId == Common.LightsIds.ALARM_BUZZER:
            return self._Buzer[2]
        elif lightId == Common.LightsIds.AUTH_SUCCES_LED:
            return self._GreenLed[2]
        else:
            self._Log.emit('lightId not found in LightsIds', EventLog.EventType.SYSTEM_WARN)


def getGateService():
    return GateService
class _GateService:
    """
        ! SINGLETON !
        user can autentificate by rf-id, password or camera
        callback: (isOpened: boolealn) => void
    """
    def __init__(self):
        self._Log = EventLog.getLoginServise()
        self._isBloking = False
        self._isOpen = False
        self._slaveService = SlaveService.getSlaveService()

    def openFor(self, milis):
        if self._isOpen:
            return
        self._open()

        def tryClose():
            while(self._isBloking):
                time.sleep(0.5)
            self._close()
            self._Log.emit('Gate State Change', EventLog.EventType.LOG, pld=False)
        t = threading.Timer(milis /1000, tryClose)
        t.setDaemon(True)
        t.start()

        self._Log.emit('Gate State Change', EventLog.EventType.LOG, pld=True)

    def isBloking(self):
        return self._isBloking

    def isOpen(self):
        return self._isOpen

    def _open(self):
        self._isOpen = True
        self._slaveService.openGate()

    def _close(self):
        self._isOpen = False
        self._slaveService.closeGate()


def getAuthService():
    return AuthService
class _AuthService:
    """
        ! SINGLETON !
        user can autentificate by rf-id, password or camera
        callback: (methond: AuthMethod) => void
    """
    def __init__(self):
        self._Log = EventLog.getLoginServise()
        self._Settings = SettingsService.getSettingsService()
        self._AfterSuccesfullAuthObservable = Common.Observable()
        self._AfterFailedAuthObservable = Common.Observable()

    def _hash(self, string):
        return hashlib.sha224(str.encode(string)).hexdigest()

    def _authFail(self):
        self._Log.emit('Auth Failed', EventLog.EventType.WARN)

    def _authSucces(self):
        self._Log.emit('Auth Succes', EventLog.EventType.LOG)


def getDisplayService():
    return DisplayService
class _DisplayService:
    """
        ! SINGLETON !
    """
    def __init__(self):
        self._Log = EventLog.getLoginServise()
        self._Schema = [
            ("Light", "UNKNOWN"),
            ("Humidity", "UNKNOWN"),
            ("Temperature", "UNKNOWN"),
            ("GateState", "Down")
        ]
        self._Timer = None

    def setShemaEntry(self, name, text):
        pass

    def showDiferentTextFor(self, textCallbackList, milis):
        pass


def getCameraService():
    return CameraService
class _CameraService:
    """
        ! SINGLETON !
    """
    def __init__(self):
        self._Log = EventLog.getLoginServise()
        self._Camera = None
        if Camera.isDepLoaded():
            self._Camera = Camera.Camera("assets/OpenCv/encode.picle")

    def getPic(self):
        self._Camera.get_pic(file_name="temp_pic.jpg")
        return "temp_pic.jpg"

    def auth(self, success_callback=None, err_callback=None):
        self._Camera.async_authorize(success_callback=success_callback, err_callback=err_callback)


""" 
====== INIT SINGLETONS ======
"""

LightService = _LightService()
UserInputs = _UserInputs()
CameraService = _CameraService()
AuthService = _AuthService()
GateService = _GateService()
DisplayService = _DisplayService()
