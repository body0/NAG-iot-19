import eventLog as EventLog

import bcrypt
import json

SettingsService = None
class _SettingsService:

    def __init__(self):
        if(SettingsService != None):
                raise Exception('Triing to instanciate singleton')

        # self._Salt = b'$2b$12$FgMh.0MG9vtsavK5rQPtKu'
        self._SettingsPath = './assets/settings.json'
        self._DefalutSettings = {
            'AccesPasswordHash': b'$2b$12$FgMh.0MG9vtsavK5rQPtKuNlfSqNaEkL2X/WaTd9wf/47/PBAn5sC',
            'SilentAlarm': False
        }

        self._Settings = self._DefalutSettings
        self._Log = EventLog.getLoginServise()

        try:
            file = open(self._SettingsPath, "r")
            self._Settings = json.load(file)
            file.close()
            self._Log.emit('SETTINGS_LOADED', EventLog.EventType.LOG)
        except FileNotFoundError:
            self._Log.emit('CANNOT_READ_SETTINGS', EventLog.EventType.SYSTEM_WARN)
        except Exception:
            self._Log.emit('CANNOT_PARSE_SETTINGS', EventLog.EventType.SYSTEM_WARN)

    def getSettings(self):
        return self._Settings

    def recomputePassword(self, password):
        salt = bcrypt.gensalt()
        hash = bcrypt.hashpw(bytes(password, 'utf-8'), salt)
        self._Settings['AccesPasswordHash'] = hash
        self.saveSettings()

    def matchAccesPassword(self, password):
        if bcrypt.checkpw(password, self._Settings['AccesPasswordHash']):
            self._Log.emit('SETTINGS_AUTH_SUCCES', EventLog.EventType.LOG)
            return True
        else:
            self._Log.emit('SETTINGS_AUTH_FAILL', EventLog.EventType.WARN)
            return False

    def saveSettings(self):
        file = open(self._SettingsPath, "w")
        json.dump(self._Settings, file)
        file.close()

SettingsService = _SettingsService()
