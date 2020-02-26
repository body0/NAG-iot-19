#include <Servo.h>

struct axis{
  byte AnalogPin, MaxAngle, MinAngle, Range;
  float Angle;
  int Treshold;

  axis(byte analogPin, byte maxAngle, byte minAngle, byte range, int treshold);
  float getAngle();
};

axis::axis(byte analogPin, byte maxAngle, byte minAngle, byte range, int treshold) {
  this->AnalogPin = analogPin;
  this->MaxAngle = maxAngle;
  this->MinAngle = minAngle;
  this->Range = range;
  this->Treshold = treshold;
  this->Angle = 90;
  
}

float axis::getAngle() {
  
  if(analogRead(AnalogPin) < (Treshold - Range)) {
    this->Angle += 0.5;
    if(Angle >= MaxAngle){
      this->Angle = MaxAngle;
    }
    
  }else if(analogRead(AnalogPin) > (Treshold + Range)) {
    Angle -= 0.5;
    if(Angle <= MinAngle){
      this->Angle = MinAngle;
    }  
  }
  return Angle;
}


axis axis1(3, 120, 60, 100, 512);
axis axis2(2, 130, 60, 100, 512);

Servo servo1;
Servo servo2;

void setup() {
  Serial.begin(9600);
  servo2.attach(10);
  servo1.attach(9);
}

void loop() {
  servo1.write(axis1.getAngle());
  servo2.write(axis2.getAngle());
  delay(10);
}
