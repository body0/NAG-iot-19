#!/bin/bash

ssh pi@nyklPi.local "rm -r /NAG/*"
#scp -r /home/nykl/Documents/CODE/NAG-iot-19/python pi@nyklPi.local:/NAG
scp -r /home/nykl/Documents/PI/NAG/python pi@nyklPi.local:/NAG
ssh pi@nyklPi.local "python3 /NAG/python/main.py" 