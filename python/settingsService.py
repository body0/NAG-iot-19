import eventLog as EventLog

from enum import Enum
import bcrypt
import json


class SettingsKeys(Enum):
    SILENT_ALARM = 'SilentAlarm'
    OUT_LIGHT_LUM_TRIG = 'OutLightTrig'
    DISABLE_CAMWEA = 'DisableCamera'

class SettingsHashKeys(Enum):
    ACCES_PASSWORK_HASH = 'AccesPasswordHash'
    RFID_HASH = 'RFIdHash'

SettingsService = None
def getSettingsService():
    return SettingsService
class _SettingsService:

    #_SettingsPath = './assets/settings.json'
    _SettingsPath = '/NAG/python/assets/settings.json'
    _DefalutSettings = {
        'Basic': {
            SettingsKeys.SILENT_ALARM.value: False,
            SettingsKeys.DISABLE_CAMWEA.value: False,
            SettingsKeys.OUT_LIGHT_LUM_TRIG.value: 8
        },
        'Hashed': {
            SettingsHashKeys.ACCES_PASSWORK_HASH.value: '$2b$12$FgMh.0MG9vtsavK5rQPtKuNlfSqNaEkL2X/WaTd9wf/47/PBAn5sC',
            SettingsHashKeys.RFID_HASH.value: [
                '$2b$12$9tuHTR3VG/i1kbjDldEyhu01.xYasuj1WqG/s4x0PaCtuVRSYJ1y6'
            ]
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
            print('File not found')
            self._Log.emit('CANNOT_READ_SETTINGS', EventLog.EventType.SYSTEM_WARN,  pld='File Not Found')
            self.saveUsedSettings()
        except Exception:
            print('File parse err')
            self._Log.emit('CANNOT_READ_SETTINGS', EventLog.EventType.SYSTEM_WARN, pld='Unknown Err')
            self.saveUsedSettings()

    def getFrontEndSettings(self):
        return self._Settings['Basic']

    def getSettingsAtribute(self, key):
        return self._Settings['Basic'][key]
    
    def matchRfid(self, uid):
        if (not type(uid) == str) or len(uid) == 0:
            return False
        #print('IN_A', password, self._Settings)
        for hashUid in self._Settings['Hashed'][SettingsHashKeys.RFID_HASH.value]:
            if bcrypt.checkpw(uid.encode('utf-8'), hashUid.encode('utf-8')):
                print('Auth True')
                return True
        print('Auth False')
        return False

    def recomputePassword(self, password):
        salt = bcrypt.gensalt()
        hash = bcrypt.hashpw(bytes(password, 'utf-8'), salt)
        self._Settings['AccesPasswordHash'] = hash
        self.saveUsedSettings()

    def matchAccesPassword(self, password):
        if (not type(password) == str) or len(password) == 0:
            return False
        #print('IN_A', password, self._Settings)
        if bcrypt.checkpw(password.encode('utf-8'), self._Settings['Hashed'][SettingsHashKeys.ACCES_PASSWORK_HASH.value].encode('utf-8')):
            print('Auth True')
            return True
        else:
            print('Auth False')
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
