import common as Common

import datetime
import os
import requests

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

# Safely load api key from env
ApiKey = ''
if 'KEYAPI' in os.environ:
    ApiKey = os.environ['KEYAPI']

DbApiAccesToken = ''
if 'DB_API_ACCES_TOKEN' in os.environ:
    DbApiAccesToken = os.environ['DB_API_ACCES_TOKEN']


LogerService = None


def getLoginServise():
    """ global _LogerServiceInstance
    if _LogerServiceInstance == None:
        _LogerServiceInstance = _LogerService() """
    return LogerService


class _LogerService:

    MAX_RECORD_QUEUE = 20

    def __init__(self):
            if(LogerService != None):
                raise Exception('Trying to instantiate singleton!')
            self._AnyObserver = Common.Observable()
            self._NameObserverMap = {}
            self._TypeObserverMap = {
                EventType.DEBUG: Common.Observable(),
                EventType.LOG: Common.Observable(),
                EventType.READ: Common.Observable(),
                EventType.WARN: Common.Observable(),
                EventType.SYSTEM_LOG: Common.Observable(),
                EventType.SYSTEM_WARN: Common.Observable(),
                EventType.SYSTEM_ERR: Common.Observable(),
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
        for i in range(len(self._Queue)):
            event = self._Queue[i]
            if size > -1 and i >= size:
                break
            if event.Name == name:
                arr.append(event)
        return arr

    def getLastByTypeList(self, eventType, size=-1):
        arr = []
        for i in range(len(self._Queue)):
            event = self._Queue[i]
            if size > -1 and i >= size:
                break
            if event.Type == eventType:
                arr.append(event)
        return arr

    def getLastAny(self, size=-1):
        #print('arr', self._Queue)
        if size < 0:
            return self._Queue
        else:
            return self._Queue[len(self._Queue) - size: len(self._Queue) - 1]

    def getAll(self):
        #print('ALL EV', self._Queue)
        return self._Queue

    """
        register new event
    """

    def emit(self, name, eventType, pld=None):
        newEvent = Event(name, eventType, pld)
        if name in self._NameObserverMap:
            self._NameObserverMap[name].emit(newEvent)
        self._TypeObserverMap[eventType].emit(newEvent)
        self._AnyObserver.emit(newEvent)
        while len(self._Queue) > self.MAX_RECORD_QUEUE:
            self._Queue.pop(0)
        self._Queue.append(newEvent)
        #print('aft', self._Queue)


"""
    HTTP CLIENT
        - send data to server
        - auth to server
"""


def sendToUpstream(eventName, data):
    jsonData = {'value': data}
    header = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'X-Api-Key': ApiKey
    }
    print("https://api.nag-iot.zcu.cz/v2/value/" + eventName, header, jsonData)
    try:
        req = requests.post("https://api.nag-iot.zcu.cz/v2/value/" +
                            eventName, json=jsonData, headers=header)
        return req.status_code
    except Exception as e:  # time out
        print(e)
        return 500


def sendStateToBroker(appState):
    jsonData = {
        'temp': appState['TempSensor'],
        'pres': appState['PresSensor'],
        'light': appState['LightSensor'],
        'gateState': appState['Gate']['status'],
        'accesToken': DbApiAccesToken
    }
    header = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    # print("https://body0.ml/nagDbIntf/homePld", header, jsonData)
    try:
        req = requests.post("https://body0.ml/nagDbIntf/homePld", json=jsonData, headers=header)
        return req.status_code
    except Exception as e:  # time out
        print(e)
        return 500

def sendEvent(eventDirecotry):
    jsonData = {
        'name': eventDirecotry['Name'],
        'type': eventDirecotry['Type'],
        'pld': eventDirecotry['Pld'],
        'timeOfCreation': eventDirecotry['Timestamp'],
        'accesToken': DbApiAccesToken
    }
    header = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    try:
        req = requests.post("https://body0.ml/nagDbIntf/addEvent", json=jsonData, headers=header)
        return req.status_code
    except Exception as e:  # time out
        print(e)
        return 500


class Event:

    def __init__(self, name, eventType, pld):
        self.Name = name
        self.Type = eventType
        self.Pld = pld
        self.Timestamp = datetime.datetime.now().isoformat()

    def getDictionary(self):
        return {
            'Name': self.Name,
            'Type': self.Type,
            'Pld': self.Pld,
            'Timestamp': self.Timestamp
        }


"""
    LOG > informuje o běžné akci uživatele
    WARN > informuje o podezřelé/nestandartní akci uživatele
    READ > pravidelné čtení ze senzorů
    SYSTEM_LOG > informuje o běžné proběhnuté systémové akci
    SYSTEM_LOG > informuje o proběhnuté podezřelé/nestandartní systémové akci
    SYSTEM_LOG > informuje o nečekané, nepřekonatelné systémové chybě
    DEBUG > dočasné
"""
class EventType:
    DEBUG = '0'

    LOG = '1'
    READ = '2'
    WARN = '4'

    SYSTEM_LOG = '3'
    SYSTEM_WARN = '5'
    SYSTEM_ERR = '6'


""" 
    ===== INIT =====
"""

LogerService = _LogerService()
