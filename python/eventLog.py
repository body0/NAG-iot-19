""" 
    EVENT LOG

        - register every event and call aproptiet callbacks
        - log to file
        - do not init any data creation, only receve them
"""
class Loger:
    """
        lisen for event to occure, then call callback
    """
    def subscribeByName(self, name, callback):
        return
    def subscribeByType(self, eventType, callback):
        return
    def subscribeAny(self, callback):
        return

    """
        get last 'size' events (-1 for all events)
    """
    def getLastByName(self, name, size=-1):
        return
    def getLastByType(self, eventType, size=-1):
        return
    def getLastAny(self, size=-1):
        return

    """
        register new event
    """
    def emit(self, name, eventType=0):
        pass

""" @unique """
"""
    LOG > informuje o běžné akci uživatele
"""
class EventType:
    LOG = 0
    WARN = 1
    ERR = 2
    DEBUG = 3
