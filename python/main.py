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

        def onGateStateChangeCallback(state):
                pass
        gate.subscribe(onGateStateChangeCallback)

        def afterAuthSucces():
                gate.openFor(1000_00)
        def afterAuthFails():
                oled.showDiferentTextFor([lambda : 'AUTH FAIL'], 1000)
        auth.subscribe(afterAuthSucces, afterAuthFails)

# INIT I2C SENZOR
# ALL CALLVACKS
# INIT API