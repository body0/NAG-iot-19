import eventLog as EventLog
""" 
    LOW-LEVEL MANAGER FOR GPIO

        - init and ceanup of gpio
        - manage simple trigers and write to pins
        - manage all pin alocation
 """

import RPi.GPIO as IO
import sys
import time
import threading
from multiprocessing import Process

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
        self._BounceTime = bounceTime
        self._CallBacks = []
        self._Channel = channel

        def _CallEachCallback(channel):
            for fun in self._CallBacks:
                fun()

        IO.add_event_detect(channel, IO.RISING, callback=_CallEachCallback, bouncetime=self._BounceTime)

    def getState(self):
        """
        :return: state of button True>high, False>low
        """
        return IO.input(self._Channel)

    def addCallBack(self, fun):
        """
        :param fun: callbac, no argument, no returm, call when button is preesd
        """
        self._CallBacks.append(fun)

    def clear(self):
        self._CallBacks = []


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
        self._RCallBacks = []
        self._LCallBacks = []

        def rising(chn):
            time.sleep(0.002)
            inA = IO.input(self._Channels[0])
            inB = IO.input(self._Channels[1])
            if inA == 1 and inB == 0:
                for fun in self._RCallBacks:
                    fun()
                return
            elif inA == 1 and inB == 1:
                for fun in self._LCallBacks:
                    fun()
                return

        IO.add_event_detect(self._Channels[0], IO.RISING, callback=rising, bouncetime=bounceTime)

    def addMoveToLeftCallBack(self, fun):
        """
        :param fun: callbac, no argument, no returm, call when encoder move to left
        """
        self._LCallBacks.append(fun)

    def addMoveToRightCallBack(self, fun):
        """
        :param fun:callbac, no argument, no returm, call when wncoder move to right
        """
        self._RCallBacks.append(fun)

    def clear(self):
        """
        clear callbackss
        """
        self._LCallBacks = []
        self._RCallBacks = []


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
        if len(inCh) != 3 or len(outCh) != 4:
            raise ValueError("wron number of chnals")

        for i in inCh:
            IO.setup(i, IO.IN, pull_up_down=IO.PUD_DOWN)
        for i in outCh:
            IO.setup(i, IO.OUT)
        self._CallBacks = []

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

    # callback take one paremeter, the preset key in string form
    def addCallBack(self, fun):
        """
        :param fun:
        :return:
        """
        self._CallBacks.append(fun)

    def clear(self):
        """
        :return:
        """
        self._CallBacks = []


class SenzorManager:
    """
    SenzorManager Class

    asynchronously regulary update value of senzor and call callback after every update
    this mean it doesn't wait for senzor to answer, when value is required
    """
    def __init__(self, fun):
        """
        :param fun:  function to update senzor value
        """
        self.Fun = fun
        self._CallBacks = []
        self.TimerStarted = False
        self.lastVal = fun()

    def addCallBack(self, fun):
        """
        :param fun:
        :return: callback after each update, take no parameter, return nothing
        """
        self._CallBacks.append(fun)

    def getLast(self):
        """
        :return: get last value loaded from 
        """
        return self.lastVal

    def start(self, period):
        """
        start periodicly updatin values

        :param period:  update value every perion second
        :return:
        """
        def update():
            """
            :return:
            """
            self.lastVal = self.Fun()
            for fun in self._CallBacks:
                fun()
            t = threading.Timer(period, update)
            t.setDaemon(True)
            t.start()

        if self.TimerStarted:
            return
        update()

    def clearCallBack(self):
        """
        :return:
        """
        self._CallBacks = []


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
        """
        :return:
        """
        self.write(255)

    def off(self):
        """
        :return:
        """
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
