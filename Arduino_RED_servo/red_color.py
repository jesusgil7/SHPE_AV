#include <Servo.h>

Servo myServo;
char incoming;

void setup() {
  Serial.begin(9600);
  myServo.attach(9);   // Servo signal pin
  myServo.write(0);    // start position
}

void loop() {
  if (Serial.available() > 0) {
    incoming = Serial.read();

    if (incoming == 'R') {
      myServo.write(90);       // Move when red detected
    }
    else if (incoming == 'N') {
      myServo.write(0);        // Default position
    }
  }
}

