#!/bin/bash

#ssh pi@nyklPi.local "rm -r /NAG/*"
#scp -r /home/nykl/Documents/CODE/NAG-iot-19/python pi@nyklPi.local:/NAG
#scp -r /home/nykl/Documents/PI/NAG/python pi@nyklPi.local:/NAG
#ssh pi@nyklPi.local "python3 /NAG/python/main.py" 

#remoteHost='pi@80.211.204.64'
#port='4055'

#remoteHost='pi@192.168.1.179'
#port='22'
remoteHost='pi@80.211.204.64'
port='4055'
ssh -p $port $remoteHost "rm -r /NAG/*"
scp -r -P $port /home/nykl/Documents/PI/NAG/python $remoteHost:/NAG
#scp -r -P $port /home/nykl/Documents/CODE/NAG-iot-19/python $remoteHost:/NAG


#ssh  -t -x -p $port $remoteHost "python3 /NAG/python/lcdDisplayManager.py" 
#ssh  -t -x -p $port $remoteHost "export KEYAPI='nic'; python3 /NAG/python/api.py" 
#ssh  -t -x -p $port $remoteHost "export KEYAPI='nic'; python3 /NAG/python/readDebug.py" 
#ssh  -t -x -p $port $remoteHost "python3 /NAG/python/devEvent.py" 


# ssh 