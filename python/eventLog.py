""" 
    EVENT LOG

        ! SINGLETON !
        - register every event and call aproptiet callbacks
        - log to file
        - do not init any data creation, only receve them
"""
_LogerServiceInstance = None
def getLoginServise():
    global _LogerServiceInstance
    if _LogerServiceInstance == None:
        _LogerServiceInstance = _LogerService()
    return _LogerServiceInstance

class _LogerService:
    def __init__(self):
            if(_LogerServiceInstance != None):
                raise Exception('Triing to instanciate singleton')
            self.

    """
        lisen for event to occure, then call callback
    """
    def subscribeByName(self, name, callback):
        return
    def subscribeByTypeList(self, eventTypeList, callback):
        return
    def subscribeAny(self, callback):
        return

    """
        get last 'size' events (-1 for all events)
    """
    def getLastByName(self, name, size=-1):
        return
    def getLastByTypeList(self, eventTypeList, size=-1):
        return
    def getLastAny(self, size=-1):
        return

    """
        register new event
    """
    def emit(self, name, eventType=0):
        pass

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
    log.emit('SETTINGS_LOADED', EventType.LOG)
    print('post all', log.getLastAny())