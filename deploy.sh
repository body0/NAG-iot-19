#!/bin/bash

#ssh pi@nyklPi.local "rm -r /NAG/*"
#scp -r /home/nykl/Documents/CODE/NAG-iot-19/python pi@nyklPi.local:/NAG
#scp -r /home/nykl/Documents/PI/NAG/python pi@nyklPi.local:/NAG
#ssh pi@nyklPi.local "python3 /NAG/python/main.py" 

remoteHost='pi@80.211.204.64'
port='4055'
ssh -p $port $remoteHost "rm -r /NAG/*"
scp -r -P $port /home/nykl/Documents/PI/NAG/python $remoteHost:/NAG
ssh -p $port $remoteHost "python3 /NAG/python/main.py" 