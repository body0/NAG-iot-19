import devServices as DevServices
import eventLog as EventLog
import common as Common
import settingsService as SettingsService
import lib.lightSensor as LightSensor
import lib.BMP085 as BMP085

import time
"""
    BUSNIESS LOGIC
"""

# INIT ALL SERVICES


def init():
        loger = EventLog.getLoginServise()
        settings = SettingsService.getSettingsService()

        gate = DevServices.getGateService()
        # auth = DevServices.getAuthService()
        lights = DevServices.getLightService()
        userInput = DevServices.getUserInputs()

        # lights.turnOnLedFor(Common.LightsIds.ALARM_LED, 5)
        # return

        def onGateStateChangeCallback(state):
                pass

        loger.subscribeByName('Gate State Change', onGateStateChangeCallback)

        def afterAuthSucces():
                print('Succes')
                lights.turnOnForFor(Common.LightsIds.AUTH_SUCCES_LED, 1)
                gate.openFor(10)

        def afterAuthFails():
                print('Fail')
                if not settings.getSettingsAtribute(SettingsService.SettingsKeys.SILENT_ALARM):
                        lights.turnOnForFor(Common.LightsIds.ALARM_BUZZER, 1)
                lights.turnOnForFor(Common.LightsIds.ALARM_LED, 1000)
                # oled.showDiferentTextFor([lambda : 'AUTH FAIL'], 1000)
        loger.subscribeByName('Auth Failed', afterAuthFails)
        loger.subscribeByName('Auth succes', afterAuthSucces)

        def gateButtonTrig(_):
                # print('A')
                gate.openFor(10)
        userInput.subscribe(Common.InputIds.GATE_BUTTON, gateButtonTrig)

        def lightButtonTrig(_):
                #print('B')
                lights.turnOnLedFor(Common.LightsIds.IN_HOUSE, 10)
        userInput.subscribe(Common.InputIds.LIGTHS_BUTTON, lightButtonTrig)

        def pirButtonTrig(_):
                #print('C')
                if not settings.getSettingsAtribute(SettingsService.SettingsKeys.SILENT_ALARM):
                        lights.turnOnForFor(Common.LightsIds.ALARM_BUZZER, 5)
                lights.turnOnLedFor(Common.LightsIds.ALARM_LED, 5)
        userInput.subscribe(Common.InputIds.PIR_SENSOR, pirButtonTrig)

        # INIT I2C SENZOR
        print('INIT SENSORS')

        def loadLight():
                value=LightSensor.readLight()
                value=float("{0:.2f}".format(value))
                EventLog.sendToUpstream('light', value)
                print('VALUE', value)
                if value < settings.getSettingsAtribute(SettingsService.SettingsKeys.OUT_LIGHT_LUM_TRIG):
                        lights.on(Common.LightsIds.OUT_HOUSE)
                else:
                        lights.off(Common.LightsIds.OUT_HOUSE)
                loger.emit('Light', EventLog.EventType.SYSTEM_LOG, value)
                # print('Value -L', value)

        lightSensor=Common.SensorTimer(loadLight)
        lightSensor.start(1.5)

        bmp085=BMP085.BMP085()
        def loadPres():
                value=bmp085.read_pressure()
                loger.emit('Pres', EventLog.EventType.SYSTEM_LOG, value)
                # print('Value -P', value)
        pressSensor=Common.SensorTimer(loadPres)
        pressSensor.start(1.5)
        def loadTemp():
                value=bmp085.read_temperature()
                loger.emit('Temp', EventLog.EventType.SYSTEM_LOG, value)
                # print('Value -T', value)
        tempSensor=Common.SensorTimer(loadTemp)
        tempSensor.start(1.5)

# DUBUG
print('DEBUG')
init()
time.sleep(5000)
