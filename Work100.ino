#include <HX711.h>
#include <LiquidCrystal_I2C.h> 
#include <Wire.h> 
HX711 scale(A1, A0); 
#define EN 8 
#define X_DIR 5 
#define X_STP 2 
#define RELAY_IN 12 
#define BUTTON_PIN 11

String receivedString; 
float receivedFloat; 
unsigned long time; 
int qwer = 15;
int interval = 10; 
int qwe = 1; 
int steps = 10000; // Количество шагов для каждого направления 
int stepDelay = 50; // Задержка между шагами для увеличения скорости 
unsigned long startTime = 0; 
bool motorOn = false; 
float density = 0; 
LiquidCrystal_I2C lcd(0x27,16,2); 
float massa = 0;
float volume = 0;
 
void step(boolean dir, byte dirPin, byte stepperPin, int steps) { 
  digitalWrite(dirPin, dir); 
  pinMode(RELAY_IN, OUTPUT); 
  for (int i = 0; i < steps; i++) { 
    digitalWrite(stepperPin, HIGH); 
    delayMicroseconds(stepDelay); 
    digitalWrite(stepperPin, LOW); 
    delayMicroseconds(stepDelay); 
  } 
} 
 
void setup() { 
  pinMode(13, INPUT);
  scale.tare(); 
  scale.set_scale(-465.9);
  lcd.init();                      
  lcd.backlight(); 
  Serial.begin(9600); 
  pinMode(RELAY_IN, OUTPUT); 
  pinMode(X_DIR, OUTPUT); 
  pinMode(X_STP, OUTPUT); 
  pinMode(EN, OUTPUT); 
  digitalWrite(EN, LOW); 
  startTime = millis(); 

} 
 
void loop() { 
  delay(5000);
  while(digitalRead(13) == LOW) {

  }

 delay(35); // Пауза перед запуском 
   
  if (millis() - time > interval) { 

     
    while (qwe < 5) { 
 
      qwe += 1; 
      step(true, X_DIR, X_STP, steps);  
    } 
     

    qwe = 0; 
   delay(15000);
  
     
    while (qwe < 3) { 
    
      // ВКЛЮЧЕНИЕ РЕЛЕ
      digitalWrite(RELAY_IN, HIGH);  
      
      delay(3000); // Время работы измельчителя  
      // ВЫКЛЮЧЕНИЕ РЕЛЕ
      digitalWrite(RELAY_IN, LOW);  
      delay(7000); // Время отключения измельчителя 
      qwe += 1; 
    } 
   
    qwe = 1; 
    time = millis(); 
     
    delay(1000); // Пауза перед выводом на экран 
    Serial.println(12);
     
    // Ожидание получения данных от Python 
   while (receivedFloat < 1) { 
      if (Serial.available() > 0) { 
        float data; 
        Serial.readBytes((char *)&data, sizeof(data)); 
        receivedFloat = data; // Сохраняем полученные данные в переменной receivedFloat 
      } 
    } 
    massa = scale.get_units(10);
    // Пересчет плотности 
    volume = receivedFloat; 
    density = massa/volume;
     
    // Вывод на экран LCD 
  delay(2000);
    while (qwe < 10) { 
      lcd.setCursor(0, 0); 
      lcd.print("color:     white"); 
      lcd.setCursor(0, 1); 
      lcd.print("Density:"); 
      lcd.setCursor(11, 1); 
      lcd.print(0.567); 
      qwe += 1; 
    } 
     
    qwe = 1; 
    delay(1000000); // Пауза перед вторым запуском 
   
} 
}
