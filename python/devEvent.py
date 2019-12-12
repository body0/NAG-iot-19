import eventLog as EventLog

import RPi.GPIO as IO

import sys
import time
import threading
""" 
    LOW-LEVEL MANAGER FOR GPIO

        - init and ceanup of gpio
        - manage simple trigers and write to pins
        - manage all pin alocation
 """

IO.setmode(IO.BCM)


class Button:
    """
    Button Class
    """
    def __init__(self, channel, bounceTime=300):
        """
        :param channel: inpot pin
        :param bounceTime: minimum time betwen trigering
        """
        IO.setup(channel, IO.IN, pull_up_down=IO.PUD_DOWN)
        self._Channel = channel
        self._InterObs = Common.MemObservable()

        def emit(channel):
            self._InterObs.emit(True)

        IO.add_event_detect(channel, IO.RISING, callback=emit, bouncetime=bounceTime)

    def getState(self):
        """
        :return: state of button True>high, False>low
        """
        return IO.input(self._Channel)

    def subscribe(self, fun):
        self._CallBacks.append(fun)

    def clearAllSubscriptions(self):
        self._InterObs = Common.MemObservable()

class RotEnc:
    """
    RotEnc Class
    """
    def __init__(self, channelA, channelB, bounceTime=150):
        """
        :param channelA: input pin A
        :param channelB: input pin B
        :param int bounceTime: minimum time betwen trigering
        """
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
    Class NumBoard
    """
    def __init__(self, inCh, outCh, bounceTime=500):
        """
        :param inCh: list of pin conected to colums in order of 1 to 3
        :param outCh: list of pin conected to colums in order of 1 to 4
        :param bounceTime:
        """
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

            for fun in self._CallBacks:
                fun(table[foundCor[0]][foundCor[1]])

        setAllOut(1)
        for i in inCh:
            IO.add_event_detect(i, IO.RISING, callback=_interupt, bouncetime=bounceTime)

    def subscribe(self, fun):
        self._CallBacks.append(fun)        

    def clear(self):
        self._InterObs = Common.MemObservable()

class LED:
    """
    LED Class
    """
    def __init__(self, channel, frequency=50):
        """
        :param channel:
        :param int frequency:
        """
        IO.setup(channel, IO.OUT)
        self.PWM = IO.PWM(channel, frequency)
        self.PWM.start(0)
        self.Intensity = 0

    def write(self, intensity):
        """
        set led brightness according to intensity parameter (0 - 255)

        :param int intensity:  range from 0 to 255
        :return:
        """
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

def wait_for_interrupts():
    """
    wait until callbacks are ivoked or program is terminated (then init clean up step)
    """
    eventLoger = EventLog.LogerService()
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
    finally:
        print("INFO: cleaning ...")
        eventLoger.emit('CLEANING', EventLog.EventType.SYSTEM_LOG)
        IO.cleanup()
