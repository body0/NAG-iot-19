import eventLog as EventLog

class EventSinkAppState:
    def __init__(self):
        self.SystemState = {
            "GateState": False,
            "Hum": -1
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