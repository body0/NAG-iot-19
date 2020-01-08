import devServices as DevServices
import eventLog as EventLog
import common as Common
import settingsService as SettingsService
import lib.lightSensor as LightSensor
import lib.BMP085 as BMP085

import time
import threading
"""
    "BUSNIESS" LOGIC
        - zde se registrují všechny enenty na buttony a senzory a jejich efekty na dům 

"""

# INIT ALL SERVICES
loger = EventLog.getLoginServise()
settings = SettingsService.getSettingsService()

gate = DevServices.getGateService()
auth = DevServices.getAuthService()
lights = DevServices.getLightService()
userInput = DevServices.getUserInputsService()

def init():
        initBusic()
        sensorInit()
        initDisplay()

def initBusic():
        # After login wait 60s, then log out
        authTimer = None
        def afterAuthSucces(_):
                nonlocal authTimer
                if authTimer != None:
                        authTimer.cancel()
                # for duration of authorization turn on green led
                lights.on(Common.LightsIds.AUTH_SUCCES_LED)

                def unAuth():
                        auth.unAuth()
                        lights.off(Common.LightsIds.AUTH_SUCCES_LED)
                        lights.turnOnLedFor(Common.LightsIds.ALARM_BUZZER, 0.5)

                t = threading.Timer(60, unAuth)
                t.setDaemon(True)
                authTimer = t
                t.start()
        loger.subscribeByName('Auth Succes', afterAuthSucces)

        def afterAuthFails(_):
                if not settings.getSettingsAtribute(SettingsService.SettingsKeys.SILENT_ALARM.value):
                        lights.turnOnForFor(Common.LightsIds.ALARM_BUZZER)
                lights.turnOnForFor(Common.LightsIds.ALARM_LED)
        loger.subscribeByName('Auth Failed', afterAuthFails)
        
        def gateButtonTrig(_):
                if auth.isAuth():
                        gate.openFor(10)
                else:
                        if not settings.getSettingsAtribute(SettingsService.SettingsKeys.SILENT_ALARM.value):
                                lights.turnOnForFor(Common.LightsIds.ALARM_BUZZER)
                        lights.turnOnForFor(Common.LightsIds.ALARM_LED)   
        userInput.subscribe(Common.InputIds.GATE_BUTTON, gateButtonTrig)

        def lightButtonTrig(_):
                lights.turnOnLedFor(Common.LightsIds.IN_HOUSE, 10)
        userInput.subscribe(Common.InputIds.LIGTHS_BUTTON, lightButtonTrig)

        def pirButtonTrig(_):
                if not auth.isAuth():
                        if not settings.getSettingsAtribute(SettingsService.SettingsKeys.SILENT_ALARM.value):
                                lights.turnOnLedFor(Common.LightsIds.ALARM_BUZZER, 3)
                        lights.turnOnLedFor(Common.LightsIds.ALARM_LED, 3)
        userInput.subscribe(Common.InputIds.PIR_SENSOR, pirButtonTrig)

# INIT I2C SENZOR
def sensorInit():
         # send every 'lightReadCount' to server
        sendToUperstreamEach = 10
        lightReadCount = 0 # const
        def loadLight():
                nonlocal lightReadCount
                # read and format light value
                value=LightSensor.readLight()
                value=float("{0:.2f}".format(value))
                lightReadCount+=1

                # every 10th send to nag server
                if lightReadCount >= sendToUperstreamEach:
                        status = EventLog.sendToUpstream('light', value)
                        if not status == 200:
                                print('Cannot send')
                                loger.emit('Cannot send data to server', EventLog.EventType.SYSTEM_WARN)
                        lightReadCount = 0
                
                # turn on/off light sensot
                if value < settings.getSettingsAtribute(SettingsService.SettingsKeys.OUT_LIGHT_ON_LUM_TRIG.value) and lights.getLedState(Common.LightsIds.OUT_HOUSE) == Common.LedState.OFF:
                        lights.on(Common.LightsIds.OUT_HOUSE)
                elif value > settings.getSettingsAtribute(SettingsService.SettingsKeys.OUT_LIGHT_ON_LUM_TRIG.value) and lights.getLedState(Common.LightsIds.OUT_HOUSE) == Common.LedState.ON:
                        lights.off(Common.LightsIds.OUT_HOUSE)

                loger.emit('Light', EventLog.EventType.SYSTEM_LOG, value)

        lightSensor=Common.SensorTimer(loadLight)
        lightSensor.start(5)

        bmp085=BMP085.BMP085()
        def loadPres():
                value=bmp085.read_pressure()
                loger.emit('Pres', EventLog.EventType.SYSTEM_LOG, value)
        pressSensor=Common.SensorTimer(loadPres)
        pressSensor.start(5)
        def loadTemp():
                value=bmp085.read_temperature()
                loger.emit('Temp', EventLog.EventType.SYSTEM_LOG, value)
        tempSensor=Common.SensorTimer(loadTemp)
        tempSensor.start(5)

def initDisplay():
        display = LcdDisplayManager.LcdDisplay()
        # asynch values (aren't loaded at will)
        self._Schema = {
            "Light": "UNKNOWN",
            "Presure": "UNKNOWN",
            "Temperature": "UNKNOWN"
        }

        def setEntry(name, text):
            self._Schema[name] = str(text.Pld)
        def lineLoader(curentLine):
            return lambda: curentLine + ' ' + self._Schema[curentLine]

       loger.subscribeByName(
            'Light', lambda pld: setEntry('Light', pld))
       loger.subscribeByName(
            'Pres', lambda pld: setEntry('Presure', pld))
       loger.subscribeByName(
            'Temp', lambda pld: setEntry('Temperature', pld))
    
        auth = getAuthService()
        gate = getGateService()
        inputs = getUserInputs()

        display.addCycleLine(lineLoader('Light'))
        display.addCycleLine(lineLoader('Presure'))
        display.addCycleLine(lineLoader('Temperature'))
        display.addCycleLine(lambda: "Is Authorized " + 
            "YES" if auth.isAuth() else "No")
        display.addCycleLine(lambda: "Gate State " + "Up" if gate.isOpen() else "Down")
        display.addCycleLine(lambda: "Obsticle in gate " + 
            "YES" if inputs.getValue(Common.InputIds.IR_TRANSISTOR) == 1 else "No")
        display.addCycleLine(lambda: "Someone outside " + 
            "YES" if inputs.getValue(Common.InputIds.PIR_SENSOR) == 1 else "No")

        display.draw()

#debug
if __name__ == '__main__':
        init()
        time.sleep(50000)
