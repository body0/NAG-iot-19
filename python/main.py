import devServices as DevServices
import eventLog as EventLog
import common as Common
import settingsService as SettingsService

""" 
    BUSNIESS LOGIC
s
        - iniciace všech zařízení
        - entry point for production env
        - 
"""

# INIT ALL SERVICES
def init():
        loger = EventLog.getLoginServise()
        settings = SettingsService.getSettingsService()

        gate = DevServices.getGateService()
        #auth = DevServices.getAuthService()
        lights = DevServices.getLightService()

        def onGateStateChangeCallback(state):
                pass
        loger.subscribeByName('Gate State Change', onGateStateChangeCallback)

        def afterAuthSucces():
                lights.turnOnForFor(Common.LightsIds.AUTH_SUCCES_LED, 1000)
                gate.openFor(100000)
        def afterAuthFails():
                if not settings.getSettingsAtribute(SettingsService.SettingsKeys.SILENT_ALARM):
                        lights.turnOnForFor(Common.LightsIds.ALARM_BUZZER, 1000)
                lights.turnOnForFor(Common.LightsIds.ALARM_LED, 1000)
                #oled.showDiferentTextFor([lambda : 'AUTH FAIL'], 1000)
        loger.subscribeByName('Auth Failed', afterAuthFails)
        loger.subscribeByName('Auth succes', afterAuthSucces)

# INIT I2C SENZOR
# ALL CALLVACKS
# INIT API