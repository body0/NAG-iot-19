import common as Common
import datetime as Datetime

""" 
    EVENT LOG

        ! SINGLETON !
        - register every event and call aproptiet callbacks
        - log to file
        - do not init any data creation, only receve them

        WARN
            - subscribe: O(1)
            - getLast: O(n) // n = number of event stored in _Queue (max length = MAX_RECORD_QUEUE)
"""
_LogerServiceInstance = None
def getLoginServise():
    global _LogerServiceInstance
    if _LogerServiceInstance == None:
        _LogerServiceInstance = _LogerService()
    return _LogerServiceInstance

class _LogerService:

    MAX_RECORD_QUEUE = 20

    def __init__(self):
            if(_LogerServiceInstance != None):
                raise Exception('Triing to instanciate singleton')
            self._AnyObserver = Common.Observable()
            self._NameObserverMap = {}
            self._TypeObserverMap = {
                'LOG': Common.Observable(),
                'WARN': Common.Observable(),
                'SYSTEM_LOG': Common.Observable(),
                'SYSTEM_WARN': Common.Observable(),
                'SYSTEM_ERR': Common.Observable(),
                'DEBUG': Common.Observable(),
            }
            self._Queue = []

    """
        lisen for event to occure, then call callback
    """
    def subscribeByName(self, name, callback):
        if name not in self._NameObserverMap:
            self._NameObserverMap[name] = Common.Observable()
        return self._NameObserverMap[name].subscrie(callback)
    def subscribeByTypeList(self, eventTypeList, callback):
        return self._TypeObserverMap[eventTypeList].subscrie(callback)
    def subscribeAny(self, callback):
        return self._AnyObserver.subscrie(callback)

    """
        get last 'size' events (-1 for all events)
    """
    def getLastByName(self, name, size=-1):
        arr = []
        for event in self._Queue:
            if size > -1 and i >= size:
                break
            if event.Name == name:
                arr.append(event)
        return arr
    def getLastByTypeList(self, eventType, size=-1):
        arr = []
        for event in self._Queue:
            if size > -1 and i >= size:
                break
            if event.Type == eventType:
                arr.append(event)
        return arr
    def getLastAny(self, size=-1):
        if size < 0:
            return self._Queue
        else:
            return self._Queue[len(self._Queue) - size, len(self._Queue) - 1]

    """
        register new event
    """
    def emit(self, name, eventType=5, pld=None):
        newEvent = Event(name, eventType, pld)
        self._TypeObserverMap[eventType].emit(newEvent)
        self._NameObserverMap[name].emit(newEvent)
        self._AnyObserver.emit(newEvent)
        while len(self._Queue) > self.MAX_RECORD_QUEUE:
            self._Queue.remove(0)
        self._Queue.append(newEvent)

"""
    HTTP CLIENT

        - send data to server
        - auth to server
"""
def sendToUpstream(self, eventName, data):
    """
    :param eventName: name of variable on website
    :param data: integer data, that will be posted to server
    :return: status code
    """
    jsonData = {'value': data}
    header = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'x-Api-Key': 'qAC9kAwXDBKTc3cS'
    }
    try:
        req = requests.post("https://api.nag-iot.zcu.cz/v1/value/" + eventName, json=jsonData, headers=header)
        return req.status_code
    except:  # time out
        return 500


class Event:

    def __init__(self, name, eventType, pld):
        self.Name = name
        self.Type = eventType
        self.Pld = pld
        self.Timestamp = Datetime.datetime


"""
    LOG > informuje o běžné akci uživatele
    WARN > informuje o podezřelé/nestandartní akci uživatele
    SYSTEM_LOG > informuje o běžné proběhnuté systémové akci
    SYSTEM_LOG > informuje o proběhnuté podezřelé/nestandartní systémové akci
    SYSTEM_LOG > informuje o nečekané, nepřekonatelné systémové chybě
    DEBUG > dočasné
"""
class EventType:
    LOG = 0
    WARN = 1

    SYSTEM_LOG = 2
    SYSTEM_WARN = 3
    SYSTEM_ERR = 4

    DEBUG = 5


if __name__ == '__main__':
    log = getLoginServise()
    def myPrint(prefix):
        def prefixPrint(data):
            print(prefix, data)
        return prefixPrint
    print('pre all', log.getLastAny())
    log.subscribeAny(myPrint('sub all'))
    log.emit('debug', EventType.LOG)
    print('post all', log.getLastAny())