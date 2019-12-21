import eventLog as EventLog

class EventSinkAppState:
    def __init__(self):
        self.SystemState = {
            'Lights': {
                'House Lights': {
                    'status': False
                },
                'Alarn': {
                    'status': False
                },
                'Alarm Led': {
                    'status': False
                },
                'Green Led': {
                    'status': True
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
        def SystemStateUpdateFactory(updatedString):
            def SystemStateUpdateFactoryFunc(value):
                self.SystemState[updatedString] = value
            return SystemStateUpdateFactoryFunc

        EventLog.LogerService.subscribeByName('GateState', SystemStateUpdateFactory('GateState'))
        EventLog.LogerService.subscribeByName('Hum', SystemStateUpdateFactory('Hum'))

    def get(self, name):
        return self.SystemState[name]
    
    def getAll(self):
        return self.SystemState