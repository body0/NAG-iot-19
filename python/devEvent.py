import eventLog as EventLog
""" 
    LOW-LEVEL MANAGER FOR GPIO

        - init and ceanup of gpio
        - manage simple trigers and write to pins
        - manage all pin alocation
 """



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
