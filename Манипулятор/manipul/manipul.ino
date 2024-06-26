#include <Servo.h>
Servo dno;
Servo plecho;
Servo lokot;
Servo kist1;
Servo kist2;
Servo ruka;

int receivedFloat = 0; 

void setup() {
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
 
  
  sweep(kist2, 90, 180, 20);
  sweep(plecho, 100, 160, 20);
  sweep(lokot, 90, 170, 20);
  delay(10);
  sweep(plecho, 160, 100, 20); 
}

   void loop() {
     // Проверяем, есть ли доступные данные
     if (Serial.available() > 0) {
       // Считываем строку до символа новой строки
       String receivedString = Serial.readStringUntil('\n'); 

       // Преобразуем строку в число
       int receivedNumber = receivedString.toInt();

       // Выводим число 
       Serial.println("Получено число: " + receivedNumber); 
      if (receivedNumber > 10) {
       kist2.write(100);
       plecho.write(80);
       sweep(ruka, 180, 140, 20);
        sweep(kist2, 100, 170, 30);
        sweep(plecho, 80, 110, 20);
       sweep(dno, 0, 180, 20);
      

      } else if(receivedNumber > 7) {
       dno.write(90);
       kist2.write(100);
       plecho.write(80);
       sweep(ruka, 180, 140, 20);
       sweep(kist2, 100, 170, 30);
        sweep(plecho, 80, 110, 20);
       sweep(dno, 90, 180, 20);
      }
    sweep(kist2, 170, 120, 20);
    sweep(ruka, 140, 180, 10);
    sweep(plecho, 110, 140, 20);
      }
      delay(10000);
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
