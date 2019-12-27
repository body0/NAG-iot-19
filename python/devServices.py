import common as Common
import eventLog as EventLog
import devEvent as DevEvent
import oledManager as OledManager
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

def getUserInputs(self):
    return self.UserInputs

class _UserInputs:
    def __init__(self):
        self._LightsButton = DevEvent.Button(-1)
        self._GateButton = DevEvent.Button(-1)
        self._Log = EventLog.getLoginServise()
        # self._numPad = DevEvent.NumBoard([-1, -1, -1], [-])

        """ def _generateInputButtonTuple(pinID):
            button =  DevEvent.Button(pinID)
            observable = Common.Observable()
            button.subscribe(lambda data: observable.emit(data))
            return (button, observable) """

    def subscribe(self, inputId, callback):
        if inputId == InputIds.LIGTHS_BUTTON:
            self._LightsButton.subscribe(callback)
        elif inputId == InputIds.GATE_BUTTON:
            self._GateButton.subscribe(callback)
        elif inputId == InputIds.NUM_PAD:
            pass
        else:
            self._Log.emit('lightId not found in LightsIds', EventLog.EventType.SYSTEM_WARN)

def getLightService(self):
    return self.LightService
class _LightService:
    """
        ! SINGLETON !
        used to turn on and off
    """
    def __init__(self):
        self._Log = EventLog.getLoginServise()

        self._Buzer = [DevEvent.LED(-1), None, LedState.OFF]
        self._RedLed = [DevEvent.LED(-1), None, LedState.OFF]
        self._GreenLed = [DevEvent.LED(-1), None, LedState.OFF]
        #self._WhiteLed = [DevEvent.LED(-1), None, LedState.OFF]

    def turnOnForFor(self, lightId, milis):

        def _turnOnLedFor(led):
            if led[1] != None:
                led[1].cancel()
            led[0].on()
            led[2] = LedState.ON

            def afterLedOff():
                led[1].off()
                led[2] = LedState.OFF
                self._Log.emit('Light state change', EventLog.EventType.LOG, {
                    'name': lightId,
                    'state': False
                })

            t = threading.Timer(milis, afterLedOff)
            t.setDaemon(True)
            led[1] = t  
            self._Log.emit('Light state change', EventLog.EventType.LOG, {
                'name': lightId,
                'state': True
            })
            t.start()

        if lightId == LightsIds.MAIN_HOUSE:
            pass
        elif lightId == LightsIds.ALARM_LED:
            _turnOnLedFor(self._RedLed)
        elif lightId == LightsIds.ALARM_BUZZER:
            _turnOnLedFor(self._Buzer)
        elif lightId == LightsIds.AUTH_SUCCES_LED:
            _turnOnLedFor(self._GreenLed)
        elif lightId == LightsIds.MAIN_HOUSE:
            #_turnOnLedFor(self._WhiteLed)
            pass
        else:
            self._Log.emit('lightId not found in LightsIds', EventLog.EventType.SYSTEM_WARN)


    def _oscilateFor(self, led, name,  period=1000, rounds=5):
        def generateUpdate(roundsRemaining, newState):
            def update():
                if roundsRemaining <= 0:
                    led[0].off()
                    led[2] = LedState.OFF
                    self._Log.emit('Light state change', EventLog.EventType.LOG, pld={
                        'name': name,
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
        led[2] = LedState.OSCILATING
        self._Log.emit('Light state change', EventLog.EventType.LOG, pld={
            'name': name,
            'state': True
        })
        t = threading.Timer(period, generateUpdate(rounds * 2, False))
        t.setDaemon(True)
        t.start()

    def getLedState(self, lightId):
        if lightId == LightsIds.MAIN_HOUSE:
            pass
        elif lightId == LightsIds.ALARM_LED:
            return self._RedLed[2]
        elif lightId == LightsIds.ALARM_BUZZER:
            return self._Buzer[2]
        elif lightId == LightsIds.AUTH_SUCCES_LED:
            return self._GreenLed[2]
        else:
            self._Log.emit('lightId not found in LightsIds', EventLog.EventType.SYSTEM_WARN)

def getGateService(self):
    return self.GateService
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
        self._slaveService = getSlaveService()

    def openFor(self, milis):
        if self._isOpen:
            return
        self._isOpen = True

        def tryClose():
            while(self._isBloking):
                time.sleep(100)
            self._open()
            self._Log.emit('Gate State Change', EventLog.EventType.LOG, pld=False)
        t = threading.Timer(milis, tryClose)
        t.setDaemon(True)
        led[1] = t
        t.start()

        self._Log.emit('Gate State Change', EventLog.EventType.LOG, pld=True)

    def isBloking(self):
        return self._isBloking

    def isOpen(self):
        return self._isOpen

    def _open(self):
        self._slaveService.openGate()

    def _close(self):
        self._slaveService.closeGate()

def getAuthService(self):
    return self.AuthService
class _AuthService:
    """
        ! SINGLETON !
        user can autentificate by rf-id, password or camera
        callback: (methond: AuthMethod) => void
    """
    def __init__(self):
        self._Log = EventLog.getLoginServise()
        self._Lights = LightService()
        self.PasswordHash = '...'
        self.RfIdHash = '...'
        self._AfterSuccesfullAuthObservable = Common.Observable()
        self._AfterFailedAuthObservable = Common.Observable()

    def _hash(self, string):
        return hashlib.sha224(str.encode(string)).hexdigest()

    def _authFail(self):
        self._Log.emit('Auth Failed', EventLog.EventType.WARN)

    def _authSucces(self):
        self._Log.emit('Auth Succes', EventLog.EventType.LOG)

def getOledService(self):
    return self.OledService
class _OledService:
    """
        ! SINGLETON !
    """
    def __init__(self):
        self._Log = EventLog.getLoginServise()
        self._Oled = OledManager.OLEDManager()
        self._Schema = [
            ("Light", "UNKNOWN"),
            ("Humidity", "UNKNOWN"),
            ("Temperature", "UNKNOWN"),
            ("GateState", "Down")
        ]
        self._Timer = None

        self._Oled.clear()
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

def getCameraService(self):
    return self.CameraService

class _CameraService:
    """
        ! SINGLETON !
    """
    def __init__(self):
        self._Log = EventLog.getLoginServise()
        self._Camera = Camera.Camera("assets/OpenCv/encode.picle")

    def getPic(self):
        self._Camera.get_pic(file_name="temp_pic.jpg")
        return "temp_pic.jpg"

    def auth(self, success_callback=None, err_callback=None):
        self._Camera.async_authorize(success_callback=success_callback, err_callback=err_callback)

""" 
====== ENUM ======
"""

class AuthMethod:
    RFID = 0
    NUM = 1
    CAMERA = 2

class LightsIds:
    MAIN_HOUSE = 'House Lights'
    ALARM_BUZZER = 'Alarn'
    ALARM_LED = 'Alarm Led'
    AUTH_SUCCES_LED = 'Green Led'

class LedState:
    OFF = 'OFF'
    ON = 'ON'
    OSCILATING = 'BLINKING'

class InputIds:
    LIGTHS_BUTTON = 0
    GATE_BUTTON = 1
    NUM_PAD = 2

""" 
====== INIT SINGLETONS ======
"""

LightService = _LightService()
UserInputs = _UserInputs()
CameraService = _CameraService()
AuthService = _AuthService()
GateService = _GateService()
OledService = _OledService()