import common as Common
import eventLog as EventLog
import devEvent as DevEvent
import slaveService as SlaveService
import settingsService as SettingsService
#import oledManager as OledManager
import camera as Camera
import lcdDisplayManager as LcdDisplayManager

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
        self._LightsButton = DevEvent.Button(22)
        self._GateButton = DevEvent.Button(27)
        self._PirSensor = DevEvent.Button(5)
        self._IR_Transistor = DevEvent.Button(24)
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
        elif inputId == Common.InputIds.PIR_SENSOR:
            self._PirSensor.subscribe(callback)
        elif inputId == Common.InputIds.IR_TRANSISTOR:
            self._IR_Transistor.subscribe(callback)
        else:
            self._Log.emit('lightId not found in LightsIds',
                           EventLog.EventType.SYSTEM_WARN)

    def getValue(self, inputId):
        if inputId == Common.InputIds.LIGTHS_BUTTON:
            return self._LightsButton.getState()
        elif inputId == Common.InputIds.GATE_BUTTON:
            return self._GateButton.getState()
        elif inputId == Common.InputIds.PIR_SENSOR:
            return self._PirSensor.getState()
        elif inputId == Common.InputIds.IR_TRANSISTOR:
            return self._IR_Transistor.getState()
        else:
            return self._Log.emit('lightId not found in LightsIds',
                           EventLog.EventType.SYSTEM_WARN)


def getLightService():
    return LightService

class _LightService:
    """
        ! SINGLETON !
        used to turn on and off lights (led, led strip, led connected to arduino)
    """

    def __init__(self):
        self._Log = EventLog.getLoginServise()

        self._Led = {
            Common.LightsIds.IN_HOUSE.value: [DevEvent.LED(17), None, Common.LedState.OFF],
            Common.LightsIds.OUT_HOUSE.value: [DevEvent.LED(6), None, Common.LedState.OFF],
            Common.LightsIds.AUTH_SUCCES_LED.value: [DevEvent.LEDZeroLogic(23), None, Common.LedState.OFF],
            Common.LightsIds.ALARM_LED.value: [DevEvent.LEDZeroLogic(18), None, Common.LedState.OFF],
            Common.LightsIds.ALARM_BUZZER.value: [
                DevEvent.LED(15), None, Common.LedState.OFF]
        }
        #self._WhiteLed = [DevEvent.LED(-1), None, LedState.OFF]

    def turnOnLedFor(self, lightId, onFor):
        def _turnOnLedFor(led):
            if led[1] != None:
                led[1].cancel()
            print('on')
            led[0].on()
            led[2] = Common.LedState.ON

            def afterLedOff():
                print('off', led)
                led[0].off()
                led[2] = Common.LedState.OFF
                self._Log.emit('Light state change', EventLog.EventType.LOG, {
                    'name': lightId,
                    'state': False
                })

            t = threading.Timer(onFor, afterLedOff)
            t.setDaemon(True)
            led[1] = t
            self._Log.emit('Light state change', EventLog.EventType.LOG, {
                'name': lightId,
                'state': True
            })
            t.start()

        if (lightId == Common.LightsIds.IN_HOUSE or
            lightId == Common.LightsIds.OUT_HOUSE or
            lightId == Common.LightsIds.ALARM_BUZZER or
            lightId == Common.LightsIds.ALARM_LED or
                lightId == Common.LightsIds.AUTH_SUCCES_LED):
            _turnOnLedFor(self._Led[lightId.value])
        else:
            self._Log.emit('lightId not found in LightsIds',
                           EventLog.EventType.SYSTEM_WARN)

    def turnOnForFor(self, lightId, period=1000, rounds=5):
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
                        t = threading.Timer(period, generateUpdate(
                            roundsRemaining - 1, not newState))
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

        if (lightId == Common.LightsIds.IN_HOUSE or
            lightId == Common.LightsIds.OUT_HOUSE or
            lightId == Common.LightsIds.ALARM_BUZZER or
            lightId == Common.LightsIds.ALARM_LED or
                lightId == Common.LightsIds.AUTH_SUCCES_LED):
            _oscilateFor(self._Led[lightId.value])
        else:
            self._Log.emit('lightId not found in LightsIds',
                           EventLog.EventType.SYSTEM_WARN)

    def getLedState(self, lightId):
        if (lightId == Common.LightsIds.IN_HOUSE or
            lightId == Common.LightsIds.OUT_HOUSE or
            lightId == Common.LightsIds.ALARM_BUZZER or
            lightId == Common.LightsIds.ALARM_LED or
                lightId == Common.LightsIds.AUTH_SUCCES_LED):
            self._Led[lightId.value][2]
        else:
            self._Log.emit('lightId not found in LightsIds',
                           EventLog.EventType.SYSTEM_WARN)

    def on(self, lightId):
        if (lightId == Common.LightsIds.IN_HOUSE or
            lightId == Common.LightsIds.OUT_HOUSE or
            lightId == Common.LightsIds.ALARM_BUZZER or
            lightId == Common.LightsIds.ALARM_LED or
                lightId == Common.LightsIds.AUTH_SUCCES_LED):
            self._Led[lightId.value][0].on()
        else:
            self._Log.emit('lightId not found in LightsIds',
                           EventLog.EventType.SYSTEM_WARN)
    
    def off(self, lightId):
        if (lightId == Common.LightsIds.IN_HOUSE or
            lightId == Common.LightsIds.OUT_HOUSE or
            lightId == Common.LightsIds.ALARM_BUZZER or
            lightId == Common.LightsIds.ALARM_LED or
                lightId == Common.LightsIds.AUTH_SUCCES_LED):
            self._Led[lightId.value][0].off()
        else:
            self._Log.emit('lightId not found in LightsIds',
                           EventLog.EventType.SYSTEM_WARN)


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
        self._isOpen = False
        #self._slaveService = SlaveService.getSlaveService()
        self._Servo = DevEvent.Sevro(12)
        self._close()
        self._inputs = getUserInputs()

    def openFor(self, timeOn):
        # print('In')
        if self._isOpen:
            return
        self._open()
        # print('open')

        def tryClose():
            while(self._inputs.getValue(Common.InputIds.IR_TRANSISTOR)):
                time.sleep(0.5)
            self._close()
            # print('close')
            self._Log.emit('Gate State Change',
                           EventLog.EventType.LOG, pld=False)
        t = threading.Timer(timeOn, tryClose)
        t.setDaemon(True)
        t.start()

        self._Log.emit('Gate State Change', EventLog.EventType.LOG, pld=True)

    def isOpen(self):
        return self._isOpen

    def _open(self):
        self._isOpen = True
        # self._slaveService.openGate()
        # self._Servo.write(90)
        self._Servo.open()

    def _close(self):
        self._isOpen = False
        # self._slaveService.closeGate()
        # self._Servo.write(163)
        self._Servo.close()


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
        self._RfId = DevEvent.RfId(0, 0, 25)
        settings = SettingsService.getSettingsService()

        def idLoaded(uid):
            if settings.matchAccesPassword(uid):
                self._authSucces()
            else:
                self._authFail()
        self._RfId.subscribe(idLoaded)
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
        self._Schema = {
            "Light": "UNKNOWN",
            "Presure": "UNKNOWN",
            "Temperature": "UNKNOWN",
            "Gate State": "Down"
        }
        self._Log = EventLog.getLoginServise()

        self._Log.subscribeByName(
            'Light', lambda pld: self.setEntry('Light', pld))
        self._Log.subscribeByName(
            'Pres', lambda pld: self.setEntry('Presure', pld))
        self._Log.subscribeByName(
            'Temp', lambda pld: self.setEntry('Temperature', pld))

        def gateStateChange(newState):
            if newState:
                self._Schema['Gate State'] = 'Up'
            else:
                self._Schema['Gate State'] = 'Down'

        self._Log.subscribeByName('Gate State Change', gateStateChange)

        self._Display = LcdDisplayManager.LcdDisplay()

        def lineLoader(curentLine):
            return lambda: curentLine + ' ' + self._Schema[curentLine]
        for line in self._Schema:
            #print('add line', line, self._Schema[line])
            self._Display.addCycleLine(lineLoader(line))
        self._Display.draw()
        """ def reDraw():
            self._Display.draw()
        displayTimer = Common.SensorTimer(reDraw)
        displayTimer.start(5) """

    def setEntry(self, name, text):
        #print('SET', name, text.Pld)
        self._Schema[name] = str(text.Pld)
        # self._Display.draw()

    def showDiferentTextFor(self, textCallbackList, milis):
        self._Display.overwriteMsg(textCallbackList)


def getCameraService():
    return CameraService


class _CameraService:
    """
        ! SINGLETON !
    """

    def __init__(self):
        self._Log = EventLog.getLoginServise()
        self._Camera = None
        if Camera.isCameraReady():
            self._Camera = Camera.Camera("assets/OpenCv/encode.picle")

    def getPic(self):
        self._Camera.get_pic(file_name="temp_pic.jpg")
        return "temp_pic.jpg"

    def auth(self, success_callback=None, err_callback=None):
        self._Camera.async_authorize(
            success_callback=success_callback, err_callback=err_callback)


""" 
====== INIT SINGLETONS ======
"""

LightService = _LightService()
UserInputs = _UserInputs()
CameraService = _CameraService()
AuthService = _AuthService()
GateService = _GateService()
DisplayService = _DisplayService()


if __name__ == "__main__":
    GateService._open()
    # DisplayService.setEntry()
    """ time.sleep(10)
    GateService._close()
    time.sleep(20) """
