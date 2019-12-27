import devServices as DevServices
import eventLog as EventLog

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

        gate = DevServices.getGateService()
        auth = DevServices.getAuthService()
        lights = DevServices.getLightService()

        def onGateStateChangeCallback(state):
                pass
        loger.subscribeByName('Gate State Change', onGateStateChangeCallback)

        def afterAuthSucces():
                lights.turnOnForFor(DevServices.LightsIds.AUTH_SUCCES_LED, 1000)
                gate.openFor(100000)
        def afterAuthFails():
                lights.turnOnForFor(DevServices.LightsIds.ALARM_BUZZER, 1000)
                lights.turnOnForFor(DevServices.LightsIds.ALARM_LED, 1000)
                #oled.showDiferentTextFor([lambda : 'AUTH FAIL'], 1000)
        loger.subscribeByName('Auth Failed', afterAuthFails)
        loger.subscribeByName('Auth succes', afterAuthSucces)

# INIT I2C SENZOR
# ALL CALLVACKS
# INIT API