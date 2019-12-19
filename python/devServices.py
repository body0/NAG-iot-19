import common as Common
import eventLog as EventLog
import devEvent as DevEvent
import oledManager as OledManager
import camera as Camera

import sys
import time
import threading

import hashlib

""" 
    COMPLEX EXTERNAL DEVICE
        
        - Define higher-level senzor information and pin numbers
        - Do not define data flow betwen service and upstream 
        - Classes
            - GateService (service)
            - AuthService (service)
            - SlaveSrvice (service)
            
            - Oled (wraper)
            - Camera (wraper)
            - SensorTimer (base class for each sensor, that needs to be periodicly updated)
"""

ServiceFactory = None
class _ServiceFactory:

    def __init__(self):
            if(ServiceFactory != None):
                raise Exception('Triing to instanciate singleton')

            self.SlaveService = SlaveService()
            self.LightService = LightService()
            self.GateService = GateService()
            self.AuthService = AuthService()
            self.OledService = OledService()
            self.CameraService = CameraService()
            self.UserInputs = UserInputs()

    def getSlaveService(self):
        return self.SlaveService
    class SlaveService:
        """
            ! SINGLETON !
            used to comunicate with arduino
        """
        def __init__(self):
            self.adress = 0xAA
            self.bus = smbus.SMBus(0)
            
        def ledOn(self, led = 0):         
			if led < 16:
				self.bus.write_byte(self.adress, SlaveCommands.LED_ON | led)
			else:
				raise Exception("Leds : Invalid number!")
		
		def ledOff(self, led = 0):
			if led < 16:
				self.bus.write_byte(self.adress, SlaveCommands.LED_OFF | led)
			else:
				raise Exception("Leds : Invalid number!")
					
		def gate(self, position = "CLOSE"):
			if position == "CLOSE":
				self.bus.write_byte(self.adress, SlaveCommands.GATE)
			elif position == "OPEN":
				self.bus.write_byte(self.adress, SlaveCommands.GATE | 0x0F)
			else:
				raise Exception("Gate: Invalid position!")
			
	def getSlaveLED(self):
		return self.SlaveLED
	class SlaveLED:
		def __init__(self, index):
			self.index = index
			self.led = SlaveService()
			
		def on(self):
			self.led.ledOff(index)
		
		def off(self):
			self.led.ledOn(index)
			 
	def getSlaveGate(self):
		return self.SlaveGate
	class SlaveGate:
		def __init_(self):
			self.gate = SlaveService()
			
		def open(self):
			self.gate.gate(OPEN)
			
		def close(self):
			self.gate.gate(CLOSE)	
			
						
    def getUserInputs(self):
        return self.UserInputs
    class UserInputs:
        def __init__(self):
            self._LightsButton = DevEvent.Button(-1)
            self._GateButton = DevEvent.Button(-1)
            # self._numPad = DevEvent.NumBoard([-1, -1, -1], [-])

            """ def _generateInputButtonTuple(pinID):
                button =  DevEvent.Button(pinID)
                observable = Common.Observable()
                button.subscribe(lambda data: observable.emit(data))
                return (button, observable) """

        def subscribe(self, inputId, callback):
            if inputId == InputIds.LIGTHS_BUTTON:
                self._LightsButton.subscribe(callback)
            elif inputId == InputIds.GATE_BUTTON:
                self._GateButton.subscribe(callback)
            elif inputId == InputId.NUM_PAD:
                pass
            else:
                self._Log.emit('lightId not found in LightsIds', EventLog.EventType.SYSTEM_WARN)
    
    def getLightService(self):
        return self.LightService
    class LightService:
        """
            ! SINGLETON !
            used to turn on and off 
        """
        def __init__(self):
            self._Log = EventLog.LogerService()
            self._Buzer = (DevEvent.LED(-1), None)
            self._RedLed = (DevEvent.LED(-1), None)
            self._GreenLed = (DevEvent.LED(-1), None)
            self._WhiteLed = (DevEvent.LED(-1), None)

        def turnOnForFor(self, lightId, milis):
            if lightId == LightsIds.MAIN_HOUSE:
                pass
            elif lightId == LightsIds.ALARM_LED:
                self._turnOnLedFor(self._RedLed)
            elif lightId == LightsIds.ALARM_BUZZER:
                self._turnOnLedFor(self._Buzer)
            elif lightId == LightsIds.AUTH_SUCCES_LED:
                self._turnOnLedFor(self._GreenLed)
            elif lightId == LightsIds.LIGHT:
                self._turnOnLedFor(self.WhiteLed)
            else:
                self._Log.emit('lightId not found in LightsIds', EventLog.EventType.SYSTEM_WARN)
        
        def _turnOnLedFor(self, led):
            led[0].on()
            if led[1] != None:
                led[1].cancel()

            t = threading.Timer(milis, lambda : led[1].off())
            t.setDaemon(True)
            self.led[1] = t
            t.start()

    def getGateService(self):
        return self.GateService
    class GateService:
        """
            ! SINGLETON !
            user can autentificate by rf-id, password or camera
            callback: (isOpened: boolealn) => void
        """
        def __init__(self):
            self._Log = EventLog.LogerService()
            self._OnGateStateChangeObserver = Common.Observable()
            self._isBloking = False
            self._isOpen = False

        def subscribe(self, onGateStateChangeCallback):
            self._OnGateStateChangeObserver.subscrie(onGateStateChangeCallback)
        
        def clearAllSubscriptions(self):
            self._AfterSuccesfullAuthObservable = Common.Observable()
            self._AfterFailedAuthObservable = Common.Observable()

        def openFor(self, milis):
            pass

        def isBloking(self):
            return self._isBloking

        def isOpen(self):
            return self._isOpen

    def getAuthService(self):
        return self.AuthService
    class AuthService:
        """
            ! SINGLETON !
            user can autentificate by rf-id, password or camera
            callback: (methond: AuthMethod) => void
        """
        def __init__(self):
            self._Log = EventLog.LogerService()
            self._Lights = LightService()
            self.PasswordHash = '...'
            self.RfIdHash = '...'
            self._AfterSuccesfullAuthObservable = Common.Observable()
            self._AfterFailedAuthObservable = Common.Observable()

            
            

        def subscribe(self, afterSuccesfullAuthCallback, afterFailedAuthCallback):
            self._AfterSuccesfullAuthObservable.subscribe(afterSuccesfullAuthCallback) 
            self._AfterFailedAuthObservable.subscribe(afterFailedAuthCallback)
        
        def clearAllSubscriptions(self):
            self._AfterSuccesfullAuthObservable = Common.Observable()
            self._AfterFailedAuthObservable = Common.Observable()
        
        def _hash(self, string):
            return hashlib.sha224(str.encode(string)).hexdigest()

        def _authFail():
            self._Lights.turnOnForFor(LightsIds.ALARM_BUZZER, 1000)
            self._Lights.turnOnForFor(LightsIds.ALARM_LED, 1000)
            self._Log.emit('AUTH FAIL', EventLog.EventType.WARN)

        def _authSucces():
            self._Lights.turnOnForFor(LightsIds.AUTH_SUCCES_LED, 1000)
            self._Log.emit('AUTH SUCCES', EventLog.EventType.LOG)

    def getOledService(self):
        return self.OledService 
    class OledService:
        """
            ! SINGLETON !
        """
        def __init__(self):
            self._Log = EventLog.LogerService()
            self._Oled = OledManager.OLEDManager()
            self._Schema = [
                ("Light", "UNKNOWN"),
                ("Humidity", "UNKNOWN"),
                ("Temperature", "UNKNOWN"),
                ("GateState", "Down")
            ]
            self._Timer = None

            self._Oled.clear()
            for entry in self._Schema:
                self._Oled.addLineCallback(lambda : entry[0] + ': ' + str(entry[1]))
        
        def setShemaEntry(self, name, text):
            for entry in self._Schema:
                if(entry[0] == name):
                    entry[1] = text
                    return True
            return False
        
        def showDiferentTextFor(self, textCallbackList, milis):
            if self._Timer != None:
                self._Timer.cancel()

            self._Oled.claer()
            for fun in textCallbackList:
                self._Oled.addLineCallback(fun)

            t = threading.Timer(milis, update)
            t.setDaemon(True)
            self._Timer = t
            t.start()

            def update():
                self._Oled.claer()
                for entry in self._Schema:
                    self._Oled.addLineCallback(lambda : entry[0] + ': ' + str(entry[1]))
                self._Timer = None

    def getCameraService(self):
        return self.CameraService
    class CameraService:
        """
            ! SINGLETON !
        """
        def __init__(self):
            self._Log = EventLog.LogerService()
            self._Camera = Camera.Camera("assets/OpenCv/encode.picle")
        
        def getPic(self):
            self.camera.get_pic(file_name="temp_pic.jpg")
            return "temp_pic.jpg"

        def auth(self, success_callback=None, err_callback=None):
            self.camera.async_authorize(success_callback=success_callback, err_callback=err_callback)

ServiceFactory = _ServiceFactory()

class AuthMethod:
    RFID = 0
    NUM = 1
    CAMERA = 2

class LightsIds:
    MAIN_HOUSE = 0
    ALARM_BUZZER = 1
    ALARM_LED = 2
    AUTH_SUCCES_LED = 3  

class InputIds:
    LIGTHS_BUTTON = 0
    GATE_BUTTON = 1
    NUM_PAD = 2

class SlaveCommands:
	LED_ON = 0x10 
	LED_OFF = 0x20	
	GATE = 0x30
	
	
class SensorTimer:
    def __init__(self, loadNewValCallback):
        self._InterObs = Common.MemObservable()
        self._LoadNewValCallback = loadNewValCallback
        self._Timer = None

    def subscribe(self, callback):
        self._InterObs.subscrie(callback)

    """
        start periodicly calling init callback in new thread
        :param period:  update value every 'perion' second
    """
    def start(self, period):
        def update():
            newVal = self._LoadNewValCallback()
            self._InterObs.emit(newVal)
            t = threading.Timer(period, update)
            t.setDaemon(True)
            self._Timer = t
            t.start()

        if self._Timer == None:
            return
        update()

    def stopAndClearAllSubscriptions(self):
        self._Timer.cancel()
        self._Timer == None
        self._InterObs = Common.MemObservable()
        pass
