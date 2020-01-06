import eventLog as EventLog
import common as Common

import datetime

class EventSinkAppState:

    DefaultState = {
        'Lights': {
            'House Lights Inside': {
                'status': False
            },
            'House Lights Outside': {
                'status': False
            },
            'Alarm': {
                'status': False
            },
            'Alarm Led': {
                'status': False
            },
            'Green Led': {
                'status': False
            }
        },
        'Gate': {
            'status': False,
            'lastOpened': '1970-01-01T00:00:00'
        },
        'LastSuccesfullAuth': '1970-01-01T00:00:00',
        'LastFailedAuth': '1970-01-01T00:00:00',
        'IsAuth': False,
        'LightSensor': -1,
        'HumSensor': -1,
        'PresSensor': -1
    }

    def __init__(self):
        self.SystemState = self.DefaultState
        self._Loger = EventLog.getLoginServise()

        def systemStateUpdateFactory(updatedString):
            def systemStateUpdateFactoryFunc(value):
                self.SystemState[updatedString] = value
                self.emitUpdateEvent()
            return systemStateUpdateFactoryFunc

        def lightUpdate(lightInfo):
            if (not hasattr(lightInfo, 'name') or 
                lightInfo.name not in self.SystemState['Lights'] or 
                not hasattr(lightInfo, 'state')):
                self._Loger.emit('Wrong Light Format', EventLog.EventType.SYSTEM_WARN)
                return

            self.SystemState['Lights'][lightInfo.name] = {
                'status': lightInfo.status.value
            }
            self.emitUpdateEvent()

        def updateGate(state):
            self.SystemState['Gate'] = {
                'status': state,
                'lastOpened': datetime.datetime.now().isoformat()
            }
            self.emitUpdateEvent()
        
        def logIn():
            self.SystemState['IsAuth'] = True
            self.SystemState['LastSuccesfullAuth'] = datetime.datetime.now().isoformat()
        def logOut():
            self.SystemState['IsAuth'] = False
        def logInFaill():
            self.SystemState['LastFailedAuth'] = datetime.datetime.now().isoformat()

        self._Loger.subscribeByName('Gate State Change', updateGate)
        self._Loger.subscribeByName('Hum', systemStateUpdateFactory('HumSensor'))
        self._Loger.subscribeByName('Light', systemStateUpdateFactory('LightSensor'))
        self._Loger.subscribeByName('Pres', systemStateUpdateFactory('PresSensor'))
        self._Loger.subscribeByName('Light state change', lightUpdate)
        self._Loger.subscribeByName('Auth Suspended', logOut)
        self._Loger.subscribeByName('Auth Succes', logIn)
        self._Loger.subscribeByName('Auth Failed', logInFaill)

    def get(self, name):
        return self.SystemState[name]
    
    def getAll(self):
        return self.SystemState

    def emitUpdateEvent(self):
        self._Loger.emit('Settings Change', EventLog.EventType.LOG)