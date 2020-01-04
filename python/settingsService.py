import eventLog as EventLog

from enum import Enum
import bcrypt
import json


class SettingsKeys(Enum):
    SILENT_ALARM = 'SilentAlarm'

class SettingsHashKeys(Enum):
    ACCES_PASSWORK_HASH = 'AccesPasswordHash'
    RFID_HASH = 'RFIdHash'

SettingsService = None
def getSettingsService():
    return SettingsService
class _SettingsService:

    _SettingsPath = './assets/settings.json'
    _DefalutSettings = {
        'Basic': {
            SettingsKeys.SILENT_ALARM.value: False
        },
        'Hashed': {
            SettingsHashKeys.ACCES_PASSWORK_HASH.value: '$2b$12$FgMh.0MG9vtsavK5rQPtKuNlfSqNaEkL2X/WaTd9wf/47/PBAn5sC',
            SettingsHashKeys.RFID_HASH.value: '...'
        }
    }

    def __init__(self):
        if(SettingsService != None):
                raise Exception('Triing to instanciate singleton')

        self._Settings = self._DefalutSettings
        self._Log = EventLog.getLoginServise()

        try:
            file = open(self._SettingsPath, "r")
            self._Settings = json.load(file)
            print('Settings Loaded', self._Settings)
            file.close()
            self._Log.emit('SETTINGS_LOADED', EventLog.EventType.LOG)
        except FileNotFoundError:
            self._Log.emit('CANNOT_READ_SETTINGS', EventLog.EventType.SYSTEM_WARN,  pld='File Not Found')
        except Exception:
            self._Log.emit('CANNOT_READ_SETTINGS', EventLog.EventType.SYSTEM_WARN, pld='Unknown Err')
            self.saveUsedSettings()

    def getFrontEndSettings(self):
        return self._Settings['Basic']

    def getSettingsAtribute(self, key):
        return self._Settings['Basic'][key]
    
    def matchRfid(self, id):
        pass

    def recomputePassword(self, password):
        salt = bcrypt.gensalt()
        hash = bcrypt.hashpw(bytes(password, 'utf-8'), salt)
        self._Settings['AccesPasswordHash'] = hash
        self.saveUsedSettings()

    def matchAccesPassword(self, password):
        print('Triing auth', password, self._Settings['Hashed'][SettingsHashKeys.ACCES_PASSWORK_HASH.value])
        if (not type(password) == str) or len(password) == 0:
            return False
        #print('IN_A', password, self._Settings)
        #print(self._Settings['Hashed'][SettingsHashKeys.ACCES_PASSWORK_HASH.value].encode('utf-8'))
        if bcrypt.checkpw(password.encode('utf-8'), self._Settings['Hashed'][SettingsHashKeys.ACCES_PASSWORK_HASH.value].encode('utf-8')):
            self._Log.emit('SETTINGS_AUTH_SUCCES', EventLog.EventType.LOG)
            print('IN True')
            return True
        else:
            self._Log.emit('SETTINGS_AUTH_FAILL', EventLog.EventType.WARN)
            print('IN False')
            return False

    def saveNewSettings(self, newSettings):
        if not testJsonStructure(newSettings):
            raise Exception('Wrong Settings')

        self._Settings['Basic'] = newSettings
        self.saveUsedSettings()

    def saveUsedSettings(self):
        try:
            file = open(self._SettingsPath, "w")
            json.dump(self._Settings, file)
            file.close()
            self._Log.emit('SETTINGS_WRITE', EventLog.EventType.LOG)
        except Exception:
            self._Log.emit('CANNOT_WRITE_SETTINGS', EventLog.EventType.SYSTEM_WARN, pld='Unknown Err')

SettingsService = _SettingsService()

def testJsonStructure(jsonObj):
    for settingsKey in SettingsKeys:
        if settingsKey.value not in jsonObj:
            return False
    """ if SettingsKeys.SILENT_ALARM.value not in jsonObj:
        return False """
    return True
