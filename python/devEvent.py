import eventLog as EventLog
import common as Common

import RPi.GPIO as IO
from mfrc522 import MFRC522 
import spidev
import pigpio

import math
import sys
import time
import threading
import atexit
"""
    LOW-LEVEL MANAGER FOR GPIO

        - init and ceanup of gpio
        - manage simple trigers and write to pins
 """

IO.setmode(IO.BCM)


class Button:
    """
        param channel: pin ID 
        param bounceTime: minimum time betwen trigering
    """
    def __init__(self, channel, bounceTime=300, hasPullDown=True):
        if hasPullDown:
            IO.setup(channel, IO.IN, pull_up_down=IO.PUD_DOWN)
        else:
            IO.setup(channel, IO.IN)
        self._Channel = channel
        self._InterObs = Common.MemObservable()

        def emit(channel):
            self._InterObs.emit(True)

        IO.add_event_detect(channel, IO.RISING, callback=emit, bouncetime=bounceTime)

    """
        return: state of button True>high, False>low
    """
    def getState(self):
        return IO.input(self._Channel)

    def subscribe(self, fun):
        return self._InterObs.subscrie(fun)

    def clearAllSubscriptions(self):
        self._InterObs = Common.MemObservable()

class RotEnc:
    """
        :param channelA: input pin A
        :param channelB: input pin B
        :param int bounceTime: minimum time betwen trigering
        -- NOT IN USE --
    """
    def __init__(self, channelA, channelB, bounceTime=150):
        IO.setup(channelA, IO.IN, pull_up_down=IO.PUD_UP)
        IO.setup(channelB, IO.IN, pull_up_down=IO.PUD_UP)
        self._Channels = (channelA, channelB)
        self._InterObsLeft = Common.MemObservable()
        self._InterObsRight = Common.MemObservable()

        def rising(chn):
            time.sleep(0.002)
            inA = IO.input(self._Channels[0])
            inB = IO.input(self._Channels[1])
            if inA == 1 and inB == 0:
                self._InterObsRight.emit(True)
                return
            elif inA == 1 and inB == 1:
                self._InterObsLeft.emit(True)
                return

        IO.add_event_detect(self._Channels[0], IO.RISING, callback=rising, bouncetime=bounceTime)

    def subscribeMoveToLeft(self, fun):
        return self._InterObsLeft.subscribe(fun)

    def subscribeMoveToRight(self, fun):
        return self._InterObsRight.subscribe(fun)

    def clearAllSubscriptions(self):
        self._InterObsLeft = Common.MemObservable()
        self._InterObsRight = Common.MemObservable()

class NumBoard:
    """
        simle num keyboard 
        :param inCh: list of pin conected to colums in order of 1 to 3
        :param outCh: list of pin conected to colums in order of 1 to 4
        -- NOT IN USE --
    """
    def __init__(self, inCh, outCh, bounceTime=500):
        self._InterObs = Common.MemObservable()

        if len(inCh) != 3 or len(outCh) != 4:
            raise ValueError("wron number of chnals")

        for i in inCh:
            IO.setup(i, IO.IN, pull_up_down=IO.PUD_DOWN)
        for i in outCh:
            IO.setup(i, IO.OUT)

        def setAllOut(value):
            for i in outCh:
                IO.output(i, value)

        def _interupt(chan):
            table = [["1", "2", "3"],
                     ["4", "5", "6"],
                     ["7", "8", "9"],
                     ["*", "0", "#"]]
            setAllOut(0)
            countFound = 0
            foundCor = None
            for oChannelId in range(len(outCh)):
                IO.output(outCh[oChannelId], 1)
                for iChannelId in range(len(inCh)):
                    if IO.input(inCh[iChannelId]):
                        countFound += 1
                        foundCor = (oChannelId, iChannelId)
                IO.output(outCh[oChannelId], 0)
            setAllOut(1)

            if countFound > 1:  # connot detect corect button
                print("WARNING: pres only one button!")
                sys.stdout.flush()
                return
            if countFound == 0:
                return

            self._InterObs.emit(table[foundCor[0]][foundCor[1]])

        setAllOut(1)
        for i in inCh:
            IO.add_event_detect(i, IO.RISING, callback=_interupt, bouncetime=bounceTime)

    def subscribe(self, fun):
        self._InterObs.subscrie(fun)        

    def clear(self):
        self._InterObs = Common.MemObservable()

class LED:
    """
        param channel: pin ID 
        param frequency: int frequency for PWM
    """
    def __init__(self, channel, frequency=50):
        IO.setup(channel, IO.OUT)
        self.PWM = IO.PWM(channel, frequency)
        self.PWM.start(0)
        self.Intensity = 0
        self.off()

    """
        param intensity: range from 0 to 255
        - set led brightness according to intensity parameter (0 - 255)
    """
    def write(self, intensity):
        if intensity > 255 or intensity < 0:  # invalid parameter
            print("WARNING: out of range")
            sys.stdout.flush()
            return
        self.Intensity = intensity / 255 * 100
        self.PWM.ChangeDutyCycle(self.Intensity)

    def on(self):
        self.write(255)

    def off(self):
        self.write(0)

class LEDZeroLogic(LED):
    def __init__(self, channel, frequency=50):
        super().__init__(channel, frequency)

    def write(self, intensity):
        super().write(255 -intensity)

    def on(self):
        self.write(255)

    def off(self):
        self.write(0)

class Sevro:
    """ 
        param channel: pin ID (best to use pin with hardware PWM suport)
    """
    def __init__(self, channel, minDutyCycle = 5, maxDutyCycle = 10):
        #IO.setup(channel, IO.OUT)
        #self.servo = IO.PWM(channel, 50) # GPIO chan for PWM with 50Hz
        #self.servo.start(7.5)

        self.minDutyCycle = minDutyCycle
        self.maxDutyCycle = maxDutyCycle
        self.pi = pigpio.pi()
        self.Channel = channel
        self.pi.set_servo_pulsewidth(self.Channel, 1000)

    def open(self):
        self.pi.set_servo_pulsewidth(self.Channel, 1000)

    def close(self):
        self.pi.set_servo_pulsewidth(self.Channel, 2070)

class RfId:
    def __init__(self, reset_pin, spi_bus=0, spi_device=0):
        self._Reader = MFRC522(bus=spi_bus, device=spi_device, pin_rst=reset_pin)
        self._IsScannig = True
        self._InterObs = Common.Observable()

        def loop():
            (status, _) = self._Reader.MFRC522_Request(self._Reader.PICC_REQIDL)

            if self._IsScannig and status == self._Reader.MI_OK:
                (status, uid) = self._Reader.MFRC522_Anticoll()

                if status == self._Reader.MI_OK:
                    print("UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3]))
                    strUID = str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3])
                    self._InterObs.emit(strUID)

        timer = Common.SensorTimer(loop)
        timer.start(0.5)

    def enable(self):
        self._IsScannig = True

    def disable(self):
        self._IsScannig = False

    def subscribe(self, callback):
        return self._InterObs.subscrie(callback)


"""
    wait until callbacks are ivoked or program is terminated (then init clean up step)
    -- NOT IN USE --
"""
def wait_for_interrupts():
    eventLoger = EventLog.getLoginServise()
    try:
        # infinite sleep on main thread
        while True:
            time.sleep(3600)
    except KeyboardInterrupt as e:
        print("PROGRAM EXIT, CTRL-C:\n{}".format(e))
        eventLoger.emit('PROGRAM EXIT', EventLog.EventType.SYSTEM_LOG)
        sys.stdout.flush()
    except Exception as e:
        print("ERROR OCCURRED:\n{}".format(e))
        eventLoger.emit('PROGRAM EXIT', EventLog.EventType.SYSTEM_ERR)
        sys.stdout.flush()
    """ finally:
        print("INFO: cleaning ...")
        eventLoger.emit('CLEANING', EventLog.EventType.SYSTEM_LOG)
        cleanup() """

#_IsCleanded = False
def cleanup():
    #global _IsCleanded
    #if _IsCleanded:
    #    return
    #_IsCleanded = True
    eventLoger = EventLog.getLoginServise()
    print("INFO: cleaning ...")
    eventLoger.emit('CLEANING', EventLog.EventType.SYSTEM_LOG)
    IO.cleanup()
    print("END")

    
atexit.register(cleanup)

if __name__ == "__main__":
    #b = Button(27)
    #b.subscribe(lambda : print('hallo'))

    rfid = RfId(0, 0, 25)
    #ser = Sevro(12)
    """ for i in range(18):
        ser.write(i * 10)
        time.sleep(0.2) """
    """     ser.write(90)
        time.sleep(1)
        ser.write(45)
        time.sleep(1)
        ser.write(0)
        time.sleep(1) """

    wait_for_interrupts()