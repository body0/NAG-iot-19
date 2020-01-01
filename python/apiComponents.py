import eventLog as EventLog
import common as Common

import datetime as Datetime

class EventSinkAppState:

    DefaultState = {
        'Lights': {
            'House Lights': {
                'status': Common.LedState.OFF.value
            },
            'Alarn': {
                'status': Common.LedState.OFF.value
            },
            'Alarm Led': {
                'status': Common.LedState.OFF.value
            },
            'Green Led': {
                'status': Common.LedState.OFF.value
            }
        },
        'Gate': {
            'status': False,
            'lastOpened': '1970-01-01T00:00:00'
        },
        'LastSuccesfullAuth': '1970-01-01T00:00:00',
        'LastFailedAuth': '1970-01-01T00:00:00',
        'LightLum': -1
    }

    def __init__(self):
        self.SystemState = self.DefaultState

        def systemStateUpdateFactory(updatedString):
            def systemStateUpdateFactoryFunc(value):
                self.SystemState[updatedString] = value
            return systemStateUpdateFactoryFunc

        def lightUpdate(lightInfo):
            if (not hasattr(lightInfo, 'name') or 
                lightInfo.name not in self.SystemState['Lights'] or 
                not hasattr(lightInfo, 'state')
            ):
                loger.emit('Wrong Light Format', EventLog.EventType.SYSTEM_WARN)
                return

            self.SystemState['Lights'][lightInfo.name] = {
                'status': lightInfo.status.value
            }

        def updateGate(state):
            self.SystemState['Gate'] = {
                'status': state,
                'lastOpened': Datetime.datetime
            }

        loger = EventLog.getLoginServise()
        loger.subscribeByName('Gate State Change', updateGate)
        loger.subscribeByName('Hum', systemStateUpdateFactory('Hum'))
        loger.subscribeByName('Light state change', lightUpdate)

    def get(self, name):
        return self.SystemState[name]
    
    def getAll(self):
        return self.SystemState