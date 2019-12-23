#include <Arduino.h>
#include <Wire.h>
#include <Servo.h>

const int I2cLocalDeviceID = 0xAA;  // My local device ID is 42
Servo servo;

unsigned char RequestedRegister;
int x;
int command;
int number;

byte ledPins[16] = {22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37};
byte gatePin = 2;

void ReceiveEvent(int howMany) {
  x = Wire.read();

}

void setup()
{
  Serial.begin(9600);
  servo.attach(gatePin);
  Wire.begin(I2cLocalDeviceID); // Initialize I2C as slave with LocalDeviceID
  Wire.onReceive(ReceiveEvent);
}

void loop()
{
  command = x & 0xF0;
  number = x & 0x0F;

  if(command == 0x10) {
    digitalWrite(ledPins[number], 1);
  }
  else if(command == 0x20) {
    digitalWrite(ledPins[number], 0);
  }
  else if(command == 0x30) {
    if(number == 0xFF) {
      servo.write(90);
    }else if(number == 0x40) {
      servo.write(0);
    }
  }
}
