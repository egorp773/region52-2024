// Включает библиотеку LiquidCrystal_I2C.
#include <LiquidCrystal_I2C.h> 
// Включает библиотеку Wire.
#include <Wire.h> 

// Определяет пины для управления шаговыми двигателями, реле и весами.
#define EN 8 
#define X_DIR 5 
#define X_STP 2 
#define RELAY_IN 12


// Включает библиотеку HX711.
#include "HX711.h"

// Устанавливает пины для датчика веса HX711.
// HX711.DOUT  - pin #A1
// HX711.PD_SCK  - pin #A0
const int HX711_DOUT_PIN = A10;
const int HX711_PD_SCK_PIN = A11;

// Создает объект scale класса HX711.
HX711 scale(HX711_DOUT_PIN, HX711_PD_SCK_PIN);

// Устанавливает коэффициент наклона для датчика веса.
// Это значение получено путем калибровки весов с известными грузами; см. README для получения подробностей
scale.set_scale(-465.9);

// Сбрасывает показания датчика веса.
scale.tare();

// Инициализирует ЖК-дисплей lcd.
LiquidCrystal_I2C lcd(0x27,16,2); 

// Включает подсветку ЖК-дисплея.
lcd.init();                      
lcd.backlight(); 

// Начинает последовательную передачу данных со скоростью 9600 бод.
Serial.begin(9600); 

// Устанавливает пин RELAY_IN как выход.
pinMode(RELAY_IN, OUTPUT); 

// Устанавливает пин X_DIR как выход.
pinMode(X_DIR, OUTPUT); 

// Устанавливает пин X_STP как выход.
pinMode(X_STP, OUTPUT); 

// Устанавливает пин EN как выход и выключает его.
pinMode(EN, OUTPUT); 
digitalWrite(EN, LOW); 

// Устанавливает начальное время для отслеживания интервалов.
unsigned long startTime = millis(); 

// Перемещает шаговый двигатель в определенном направлении указанное количество шагов.
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

// Настраивает параметры шагового двигателя.
void setup() { 

  // Начинает последовательную передачу данных со скоростью 38400 бод.
  Serial.begin(38400);

  // Устанавливает коэффициент наклона для датчика веса.
  scale.set_scale(-465.9);                      

  // Сбрасывает показания датчика веса.
  scale.tare();

  // Инициализирует ЖК-дисплей lcd.
  lcd.init();                      
  lcd.backlight(); 

  // Начинает последовательную передачу данных со скоростью 9600 бод.
  Serial.begin(9600); 

  // Устанавливает пин RELAY_IN как выход.
  pinMode(RELAY_IN, OUTPUT); 

  // Устанавливает пин X_DIR как выход.
  pinMode(X_DIR, OUTPUT); 

  // Устанавливает пин X_STP как выход.
  pinMode(X_STP, OUTPUT); 

  // Устанавливает пин EN как выход и выключает его.
  pinMode(EN, OUTPUT); 
  digitalWrite(EN, LOW); 

  // Устанавливает начальное время для отслеживания интервалов.
  startTime = millis(); 
} 

// Основной цикл программы.
void loop() { 

  // Пауза перед запуском.
  delay(20); 

  // Проверяет, прошло ли указанное количество времени с момента последнего вызова функции.
  if (millis() - time > interval) { 

    // Получение сигнала с 

    // Отправляет сообщение по последовательному порту.
    Serial.println("000000"); 

    // Перемещает шаговый двигатель влево (положительное направление) указанное количество шагов.
    while (qwe < 8) { 
      Serial.println("11111"); 
      qwe += 1; 
      step(true, X_DIR, X_STP, steps);  
    } 

    // Устанавливает реле в состояние включения.
    Serial.println("222222"); 
    qwe = 1; 

    // Включает реле.
    delay(15000); 

    // Отключает реле.
    digitalWrite(RELAY_IN, HIGH);  

    // Перемещает шаговый двигатель вправо (отрицательное направление) указанное количество шагов.
    while (qwe < 6) { 
      qwe += 1; 
      digitalWrite(RELAY_IN, LOW);    
      delay(5000); 
      delay(8000); 
    } 

    // Сбрасывает значение переменной.
    qwe = 1; 

    // Устанавливает время для отслеживания интервала.
    time = millis(); 

    // Пауза перед выводом на экран.
    delay(1000);
    // Ожидание получения данных от Python.
    while (receivedFloat < 1) { 
      if (Serial.available() > 0) { 
        float data; 
        Serial.readBytes((char *)&data, sizeof(data)); 
        receivedFloat = data; 
      } 
    } 

    // Рассчитывает плотность.
    massa = scale.get_units(10);
    density = massa / receivedFloat;
    // Выводит значение плотности на ЖК-дисплей.
    while (qwe < 10) { 
      lcd.setCursor(0, 0); 
      lcd.print("color:     white"); 
      lcd.setCursor(0, 1); 
      lcd.print("Density:"); 
      lcd.setCursor(8, 1); 
      lcd.print(density); 
      qwe += 1; 
    } 

    // Сбрасывает значение переменной.
    qwe = 1; 

    // Пауза перед вторым запуском.
    delay(1000000); 
  } 
}