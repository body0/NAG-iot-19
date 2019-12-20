import devServices as DevServices

""" 
    BUSNIESS LOGIC
s
        - iniciace všech zařízení
        - entry point for production env
        - 
"""

# INIT ALL SERVICES
def init():
        gate = DevServices.ServiceFactory.getGateService()
        auth = DevServices.ServiceFactory.getAuthService()
        oled = DevServices.ServiceFactory.getOledService()
        lights = DevServices.ServiceFactory.getLightService()

        def onGateStateChangeCallback(state):
                pass
        gate.subscribe(onGateStateChangeCallback)

        def afterAuthSucces():
                lights.turnOnForFor(DevServices.LightsIds.AUTH_SUCCES_LED, 1000)
                gate.openFor(1000_00)
        def afterAuthFails():
                lights.turnOnForFor(DevServices.LightsIds.ALARM_BUZZER, 1000)
                lights.turnOnForFor(DevServices.LightsIds.ALARM_LED, 1000)
                oled.showDiferentTextFor([lambda : 'AUTH FAIL'], 1000)
        auth.subscribe(afterAuthSucces, afterAuthFails)

# INIT I2C SENZOR
# ALL CALLVACKS
# INIT API