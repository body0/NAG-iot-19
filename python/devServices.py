import common as Common
import eventLog as EventLog
import devEvent as DevEvent
import settingsService as SettingsService
import camera as Camera
import lcdDisplayManager as LcdDisplayManager

import sys
import time
import threading

"""
    ENABLE COMPLEX ONE PURPOSE SINGLETON SERVISES

        - Define some higher-level pheriphery information and define all pin numbers
        - for more information refer to README.md
"""


LightService = None
UserInputs = None
CameraService = None
AuthService = None
GateService = None
DisplayService = None

"""
    ===== SERVICES =====
"""


def getUserInputs():
    return UserInputs
class _UserInputs:
    """ 
        ! SINGLETON !
        Define button pins and operation, can be extended by button unlike input.
    """

    def __init__(self):
        if(UserInputs != None):
            raise Exception('Trying to instantiate singleton!')
        """ 
        self._LightsButton = DevEvent.Button(22)
        self._GateButton = DevEvent.Button(27)
        self._PirSensor = DevEvent.Button(5)
        self._IR_Transistor = DevEvent.Button(24) 
        """
        self._Log = EventLog.getLoginServise()
        self._ButtonLikeInput = {
            Common.InputIds.LIGTHS_BUTTON.value: DevEvent.Button(22),
            Common.InputIds.GATE_BUTTON.value: DevEvent.Button(27),
            Common.InputIds.PIR_SENSOR.value: DevEvent.Button(5),
            Common.InputIds.IR_TRANSISTOR.value: DevEvent.Button(24)
        }
    """
        param: callback: (_:Null) => void
        return: subscription destructor
        - call callback when input activated
    """

    def subscribe(self, inputId, callback):
        if inputId.value in self._ButtonLikeInput:
            return self._ButtonLikeInput[inputId].subscribe(callback)
        else:
            self._Log.emit('LightId not found in LightsIds',
                           EventLog.EventType.SYSTEM_WARN)
    """
         return: True/False
         Return if input is active
    """

    def getValue(self, inputId):
        if inputId.value in self._ButtonLikeInput:
            return self._ButtonLikeInput[inputId].getState()
        else:
            return self._Log.emit('LightId not found in LightsIds',
                                  EventLog.EventType.SYSTEM_WARN)


def getLightService():
    return LightService
class _LightService:
    """
        ! SINGLETON !
        Used to turn on and off lights or other led like objects
    """

    def __init__(self):
        if(LightService != None):
            raise Exception('Trying to instantiate singleton!')
        self._Log = EventLog.getLoginServise()
        self._Led = {
            Common.LightsIds.IN_HOUSE.value: [DevEvent.LED(17), None, Common.LedState.OFF],
            Common.LightsIds.OUT_HOUSE.value: [DevEvent.LED(6), None, Common.LedState.OFF],
            Common.LightsIds.AUTH_SUCCES_LED.value: [DevEvent.LEDZeroLogic(23), None, Common.LedState.OFF],
            Common.LightsIds.ALARM_LED.value: [DevEvent.LEDZeroLogic(18), None, Common.LedState.OFF],
            Common.LightsIds.ALARM_BUZZER.value: [
                DevEvent.LED(19), None, Common.LedState.OFF]
        }
    """ 
        param onFor: number in second
        param lightId: value from Enum (Common.LightsIds)
        - turn on light for onFor second
    """

    def turnOnLedFor(self, lightId, onFor):
        def _turnOnLedFor(led):
            if led[1] != None:
                led[1].cancel()
            led[0].on()
            led[2] = Common.LedState.ON

            def afterLedOff():
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

        if (lightId.value in self._Led):
            _turnOnLedFor(self._Led[lightId.value])
        else:
            self._Log.emit('lightId not found in LightsIds',
                           EventLog.EventType.SYSTEM_WARN)

    """ 
        param period: delay in seconds betwen led change
        param rounds: number of turn cicle
        param lightId: value from Enum (Common.LightsIds)
        - blink light several times
    """

    def turnOnForFor(self, lightId, period=0.75, rounds=3):
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
            t = threading.Timer(
                period, generateUpdate((rounds - 1) * 2, False))
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
        if (lightId.value in self._Led):
            return self._Led[lightId.value][2]
        else:
            self._Log.emit('lightId not found in LightsIds',
                           EventLog.EventType.SYSTEM_WARN)

    def on(self, lightId):
        if (lightId.value in self._Led):
            self._Led[lightId.value][0].on()
            self._Log.emit('Light state change', EventLog.EventType.LOG, pld={
                'name': lightId,
                'state': True
            })
        else:
            self._Log.emit('lightId not found in LightsIds',
                           EventLog.EventType.SYSTEM_WARN)

    def off(self, lightId):
        if (lightId.value in self._Led):
            self._Led[lightId.value][0].off()
            self._Log.emit('Light state change', EventLog.EventType.LOG, pld={
                'name': lightId,
                'state': False
            })
        else:
            self._Log.emit('lightId not found in LightsIds',
                           EventLog.EventType.SYSTEM_WARN)


def getGateService():
    return GateService
class _GateService:

    """
        ! SINGLETON !
        DO NOT CHECK IF USER IS AUTH
    """

    def __init__(self):
        if(GateService != None):
            raise Exception('Trying to instantiate singleton!')
        self._Log = EventLog.getLoginServise()
        self._isOpen = False
        self._Servo = DevEvent.Sevro(12)
        self._close()
        self._inputs = getUserInputs()
    """
        open gate for "timeOn" second
    """

    def openFor(self, timeOn):
        if self._isOpen:
            return
        self._open()
        self._Log.emit('Gate State Change', EventLog.EventType.LOG, pld=True)

        def tryClose():
            while(self._inputs.getValue(Common.InputIds.IR_TRANSISTOR)):
                time.sleep(0.5)
            self._close()
            self._Log.emit('Gate State Change',
                           EventLog.EventType.LOG, pld=False)
        t = threading.Timer(timeOn, tryClose)
        t.setDaemon(True)
        t.start()

    def isOpen(self):
        return self._isOpen

    def _open(self):
        self._isOpen = True
        self._Servo.open()

    def _close(self):
        self._isOpen = False
        self._Servo.close()


def getAuthService():
    return AuthService
class _AuthService:
    """
        ! SINGLETON !
        user can autentificate and authorize by rf-id
    """

    def __init__(self):
        if(AuthService != None):
            raise Exception('Trying to instantiate singleton!')
        self._IsAuhtVar = False
        self._Log = EventLog.getLoginServise()
        self._RfId = DevEvent.RfId(0, 0, 25)
        self._Settings = SettingsService.getSettingsService()
        settings = SettingsService.getSettingsService()

        def idLoaded(uid):
            if settings.matchRfid(uid):
                self._authSucces()
            else:
                self._authFail()
        self._RfId.subscribe(idLoaded)

    """
         revoke authorization
    """
    def unAuth(self):
        self._IsAuhtVar = False
        self._Log.emit('Auth Suspended', EventLog.EventType.LOG)

    def isAuth(self):
        return self._IsAuhtVar

    def _authFail(self):
        self._Log.emit('Auth Failed', EventLog.EventType.WARN)

    def _authSucces(self):
        self._IsAuhtVar = True
        self._Log.emit('Auth Succes', EventLog.EventType.LOG)

def getDisplayService():
    return DisplayService


class _DisplayService:
    """
        ! SINGLETON !
         Lisen for events and update them if needed.
         Init lcdDisplayManager and let him cysle throught the data.
    """

    def __init__(self):
        self._Log = EventLog.getLoginServise()
        self._Schema = {
            "Light": "UNKNOWN",
            "Presure": "UNKNOWN",
            "Temperature": "UNKNOWN",
            "Gate State": "Down",
            # "Is Authorized": "No"
        }
        self._Log = EventLog.getLoginServise()

        """ self._Log.subscribeByName(
            'Auth Suspended', lambda pld: self.setEntry('Is Authorized', 'No')
        )
        self._Log.subscribeByName(
            'Auth Succes', lambda pld: self.setEntry('Is Authorized', 'Yes')
        ) """

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
        """ for line in self._Schema:
            self._Display.addCycleLine(lineLoader(line))"""

        auth = getAuthService()
        inputs = getUserInputs()
        self._Display.addCycleLine(lineLoader('Light'))
        self._Display.addCycleLine(lineLoader('Presure'))
        self._Display.addCycleLine(lineLoader('Temperature'))
        self._Display.addCycleLine(
            lambda: "Is Authorized " + ("YES" if auth.isAuth() else "No"))
        self._Display.addCycleLine(lineLoader('Gate State'))
        self._Display.addCycleLine(lambda: "Obsticle in gate " + (
            "YES" if inputs.getValue(Common.InputIds.IR_TRANSISTOR) == 1 else "No"))
        self._Display.addCycleLine(lambda: "Someone outside " + (
            "YES" if inputs.getValue(Common.InputIds.PIR_SENSOR) == 1 else "No"))

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
