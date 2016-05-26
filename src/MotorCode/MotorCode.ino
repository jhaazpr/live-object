// Adafruit Motor shield library
// copyright Adafruit Industries LLC, 2009
// this code is public domain, enjoy!

#include <AFMotor.h>

AF_DCMotor motor(4);
int incomingByte = 0;
void setup() {
  Serial.begin(9600);           // set up Serial library at 9600 bps
   motor.run(RELEASE);

   // Quickly start and stop to know the motor is on
   motor.run(FORWARD);
   motor.setSpeed(255);
   delay(500);
   motor.run(RELEASE);
}
void loop() {
  Serial.println("I am the motorshield.");
  if (Serial.available() > 0) {
      // read the incoming byte:
      incomingByte = Serial.read();
      Serial.print("I got" );
      Serial.println(incomingByte);
      if(incomingByte == 0 || incomingByte == 48){
         motor.run(RELEASE);
        
      }
      else if(incomingByte == 1 || incomingByte == 49){
        motor.run(FORWARD);
        motor.setSpeed(110);
      }
      else if(incomingByte == 2 || incomingByte == 50){
        motor.run(FORWARD);
        motor.setSpeed(160);
      }
      else if(incomingByte == 3 || incomingByte == 51){
        motor.run(FORWARD);
        motor.setSpeed(210);
      }
      else if(incomingByte == 4 || incomingByte == 52){
        motor.run(FORWARD);
        motor.setSpeed(255);
      }
   }
   delay(500);              // wait for a second
}
