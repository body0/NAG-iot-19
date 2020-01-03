from mfrc522 import MFRC522
import RPi.GPIO as GPIO

READER = MFRC522()
while True:
    (status, TagType) = READER.MFRC522_Request(READER.PICC_REQIDL)
    if status != READER.MI_OK:
        print('0')
        continue
    (status, uid) = READER.MFRC522_Anticoll()
    if status != READER.MI_OK:
        print('1')
        continue
    print('3', uid)