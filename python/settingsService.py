import eventLog as EventLog

from enum import Enum
import bcrypt
import json


class SettingsKeys(Enum):
    SILENT_ALARM = 'SilentAlarm',
    ACCES_PASSWORK_HASH = 'AccesPasswordHash'
    RFID_HASH = 'RFIdHash'

SettingsService = None
def getSettingsService():
    return SettingsService
class _SettingsService:

    _SettingsPath = './assets/settings.json'
    _DefalutSettings = {
        SettingsKeys.ACCES_PASSWORK_HASH: b'$2b$12$FgMh.0MG9vtsavK5rQPtKuNlfSqNaEkL2X/WaTd9wf/47/PBAn5sC',
        SettingsKeys.SILENT_ALARM: False,
        SettingsKeys.RFID_HASH: '...'
    }

    def __init__(self):
        if(SettingsService != None):
                raise Exception('Triing to instanciate singleton')

        # self._Salt = b'$2b$12$FgMh.0MG9vtsavK5rQPtKu'

        self._Settings = self._DefalutSettings
        self._Log = EventLog.getLoginServise()

        try:
            file = open(self._SettingsPath, "r")
            self._Settings = json.load(file)
            file.close()
            self._Log.emit('SETTINGS_LOADED', EventLog.EventType.LOG)
        except FileNotFoundError:
            self._Log.emit('CANNOT_READ_SETTINGS', EventLog.EventType.SYSTEM_WARN,  pld='File Not Found')
        except Exception:
            self._Log.emit('CANNOT_READ_SETTINGS', EventLog.EventType.SYSTEM_WARN, pld='Unknown Err')

    def getSettings(self):
        return self._Settings

    def getSettingsAtribute(self, key):
        return self._Settings[key]

    def recomputePassword(self, password):
        salt = bcrypt.gensalt()
        hash = bcrypt.hashpw(bytes(password, 'utf-8'), salt)
        self._Settings['AccesPasswordHash'] = hash
        self.saveUsedSettings()

    def matchAccesPassword(self, password):
        if bcrypt.checkpw(password, self._Settings['AccesPasswordHash']):
            self._Log.emit('SETTINGS_AUTH_SUCCES', EventLog.EventType.LOG)
            return True
        else:
            self._Log.emit('SETTINGS_AUTH_FAILL', EventLog.EventType.WARN)
            return False

    def saveNewSettings(self, newSettings):
        if not testJsonStructure(newSettings):
            raise Exception('Wrong Settings')

        self._Settings = newSettings
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
        if settingsKey not in jsonObj:
            return False
    return True
