import devServices as DevServices
import eventLog as EventLog
import common as Common
import settingsService as SettingsService
import lib.lightSensor as LightSensor
import lib.BMP085 as BMP085

import time
import threading
"""
    BUSNIESS LOGIC
"""

# INIT ALL SERVICES


def init():
        loger = EventLog.getLoginServise()
        settings = SettingsService.getSettingsService()

        gate = DevServices.getGateService()
        auth = DevServices.getAuthService()
        lights = DevServices.getLightService()
        userInput = DevServices.getUserInputs()

        # lights.turnOnLedFor(Common.LightsIds.ALARM_LED, 5)
        # return

        def onGateStateChangeCallback(state):
                pass

        loger.subscribeByName('Gate State Change', onGateStateChangeCallback)

        authTimer = None
        def afterAuthSucces(_):
                nonlocal authTimer
                print('Succes')
                lights.on(Common.LightsIds.AUTH_SUCCES_LED)

                def unAuth():
                        auth.unAuth()
                        lights.off(Common.LightsIds.AUTH_SUCCES_LED)
                        lights.turnOnLedFor(Common.LightsIds.ALARM_BUZZER, 0.5)

                if authTimer != None:
                        authTimer.cancel()
                t = threading.Timer(60, unAuth)
                t.setDaemon(True)
                authTimer = t
                t.start()

        def afterAuthFails(_):
                print('Fail')
                if not settings.getSettingsAtribute(SettingsService.SettingsKeys.SILENT_ALARM.value):
                        lights.turnOnForFor(Common.LightsIds.ALARM_BUZZER)
                lights.turnOnForFor(Common.LightsIds.ALARM_LED)
                # oled.showDiferentTextFor([lambda : 'AUTH FAIL'], 1000)
        loger.subscribeByName('Auth Failed', afterAuthFails)
        loger.subscribeByName('Auth Succes', afterAuthSucces)

        def gateButtonTrig(_):
                print('A')
                if auth.isAuth():
                        gate.openFor(10)
                else:
                        if not settings.getSettingsAtribute(SettingsService.SettingsKeys.SILENT_ALARM.value):
                                lights.turnOnForFor(Common.LightsIds.ALARM_BUZZER)
                        lights.turnOnForFor(Common.LightsIds.ALARM_LED)   
        userInput.subscribe(Common.InputIds.GATE_BUTTON, gateButtonTrig)

        def lightButtonTrig(_):
                #print('B')
                lights.turnOnLedFor(Common.LightsIds.IN_HOUSE, 10)
        userInput.subscribe(Common.InputIds.LIGTHS_BUTTON, lightButtonTrig)

        def pirButtonTrig(_):
                #print('C')
                if not auth.isAuth():
                        if not settings.getSettingsAtribute(SettingsService.SettingsKeys.SILENT_ALARM.value):
                                lights.turnOnLedFor(Common.LightsIds.ALARM_BUZZER, 3)
                        lights.turnOnLedFor(Common.LightsIds.ALARM_LED, 3)
        userInput.subscribe(Common.InputIds.PIR_SENSOR, pirButtonTrig)

        # INIT I2C SENZOR
        print('INIT SENSORS')

        # send every 'lightReadCount' to server
        sendToUperstreamEach = 10
        lightReadCount = 0
        def loadLight():
                nonlocal lightReadCount
                value=LightSensor.readLight()
                value=float("{0:.2f}".format(value))
                lightReadCount+=1
                if lightReadCount >= sendToUperstreamEach:
                        status = EventLog.sendToUpstream('light', value)
                        if not status == 200:
                                print('Cannot send')
                                loger.emit('Cannot send data to server', EventLog.EventType.SYSTEM_WARN)
                        lightReadCount = 0
                #print('VALUE', value)
                if value < settings.getSettingsAtribute(SettingsService.SettingsKeys.OUT_LIGHT_ON_LUM_TRIG.value) and lights.getLedState(Common.LightsIds.OUT_HOUSE) == Common.LedState.OFF:
                        lights.on(Common.LightsIds.OUT_HOUSE)
                elif value > settings.getSettingsAtribute(SettingsService.SettingsKeys.OUT_LIGHT_ON_LUM_TRIG.value) and lights.getLedState(Common.LightsIds.OUT_HOUSE) == Common.LedState.ON:
                        lights.off(Common.LightsIds.OUT_HOUSE)
                loger.emit('Light', EventLog.EventType.SYSTEM_LOG, value)
                # print('Value -L', value)

        lightSensor=Common.SensorTimer(loadLight)
        lightSensor.start(0.5)

        bmp085=BMP085.BMP085()
        def loadPres():
                value=bmp085.read_pressure()
                loger.emit('Pres', EventLog.EventType.SYSTEM_LOG, value)
                # print('Value -P', value)
        pressSensor=Common.SensorTimer(loadPres)
        pressSensor.start(2)
        def loadTemp():
                value=bmp085.read_temperature()
                loger.emit('Temp', EventLog.EventType.SYSTEM_LOG, value)
                # print('Value -T', value)
        tempSensor=Common.SensorTimer(loadTemp)
        tempSensor.start(2)

# DUBUG
print('DEBUG')
init()
time.sleep(5000)
