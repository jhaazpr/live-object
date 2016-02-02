/*
  Blink
  Turns on an LED on for one second, then off for one second, repeatedly.

  Most Arduinos have an on-board LED you can control. On the Uno and
  Leonardo, it is attached to digital pin 13. If you're unsure what
  pin the on-board LED is connected to on your Arduino model, check
  the documentation at http://www.arduino.cc

  This example code is in the public domain.

  modified 8 May 2014
  by Scott Fitzgerald
 */

int incomingByte = 0;  
int high = 6;
int med = 7;
int low = 5;
// the setup function runs once when you press reset or power the board
void setup() {
  // initialize digital pin 13 as an output.
  pinMode(low, OUTPUT);
  pinMode(med, OUTPUT);
  pinMode(high, OUTPUT);
  Serial.begin(9600);
}

// the loop function runs over and over again forever
void loop() {
  Serial.println("I am on");
  if (Serial.available() > 0) {
      // read the incoming byte:
      incomingByte = Serial.read();
      Serial.print("I got" );
      Serial.println(incomingByte);
      if(incomingByte == 0){
        digitalWrite(low, LOW);
        digitalWrite(med, LOW);
        digitalWrite(high, LOW);
      }
      else if(incomingByte == 1){
        digitalWrite(low, HIGH);
        digitalWrite(med, LOW);
        digitalWrite(high, LOW);
      }
      else if(incomingByte == 2){
        digitalWrite(low, LOW);
        digitalWrite(med, HIGH);
        digitalWrite(high, LOW);
      }
       else if(incomingByte == 3){
        digitalWrite(low, LOW);
        digitalWrite(med, LOW);
        digitalWrite(high, HIGH);
      }
   }
   delay(500);              // wait for a second
}