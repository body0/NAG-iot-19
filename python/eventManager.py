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
    try:
        while True:
            time.sleep(3600)
            # print("ttttttt")
            # sys.stdout.flush()
    except KeyboardInterrupt as e:
        print("PROGRAM EXIT, CTRL-C:\n{}".format(e))
        sys.stdout.flush()
    except Exception as e:
        print("ERROR OCCURRED:\n{}".format(e))
        sys.stdout.flush()
    finally:
        print("INFO: cleaning ...")
        IO.cleanup()
