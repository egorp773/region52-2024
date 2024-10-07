#include <Servo.h>
Servo dno;
Servo plecho;
Servo lokot;
Servo kist1;
Servo kist2;
Servo ruka;
#define BUTTON_PIN 11
float receivedFloat = 1; 
float receivedNumber = 1;

void setup() {
  pinMode(19, OUTPUT);

  dno.attach(2);
  plecho.attach(10);
  lokot.attach(8);
  kist1.attach(3);
  kist2.attach(4);
  ruka.attach(6);
  dno.write(0);
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
  ruka.write(180);
  // Начальное положение сервоприводов
 

  plecho.write(100);

  lokot.write(90);
  kist1.write(90);
  kist2.write(90);
 
  while(digitalRead(BUTTON_PIN) == LOW) {
  
}
  Serial.println(12);
  delay(500);
  sweep(kist2, 90, 180, 20);
  sweep(plecho, 100, 110, 20);
  sweep(lokot, 90, 180, 20);
  delay(10);
  sweep(plecho, 110, 90, 20); 
}

void loop() {


    while (receivedNumber < 10) {
      if (Serial.available() > 0) { 
       float data; 
       Serial.readBytes((char *)&data, sizeof(data)); 
      receivedNumber = data;

    }
    }
    //sweep(lokot, 180, 140, 20);
    sweep(kist2, 180, 90, 30);
   // sweep(lokot, 140, 180, 20 );
    delay(600);
    ruka.write(20);
    delay(1000);
    sweep(lokot, 170, 130, 30);
    sweep(kist2, 90, 180, 20);

  
    sweep(dno, 0, 180, 30);
    sweep(kist2, 180, 120, 20);
    sweep(ruka, 20, 180, 20);
    sweep(kist2, 120, 180, 20);
    digitalWrite(19, HIGH);
    sweep(dno, 180, 0, 20);
    delay(1000);

    delay(1000000000);
  }

void sweep(Servo servo, int oldPos, int newPos, int servoSpeed) {
  if (oldPos <= newPos) {
    for (oldPos; oldPos <= newPos; oldPos += 1) {
      servo.write(oldPos);
      delay(servoSpeed);
    }
  } else if (oldPos >= newPos) {
    for (oldPos; oldPos >= newPos; oldPos -= 1) {
      servo.write(oldPos);
      delay(servoSpeed);
    }
  }
}
