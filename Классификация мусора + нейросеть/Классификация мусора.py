import tensorflow as tf
from tensorflow.keras.models import load_model
import cv2
import numpy as np
import time
import serial
import struct
hx = 0
k = 1
d = 15
model = load_model("keras_Model.h5", compile=False)  # Загружаем модель
class_names = open("labels.txt", "r").readlines()  # Загружаем список классов

# Настройка порта Arduino
ser = serial.Serial('COM4', 9600)  # Создаем объект для связи с Arduino

# Открытие веб-камеры
print(1)
while k != 10:
    data = ser.readline().decode('ascii').strip()
    if data:
        number = int(data)
        print(data)
        print(1244)
        k = 10
camera = cv2.VideoCapture('http://172.20.10.12/')  # Открываем веб-камеру
    
time.sleep(5)  # Ждем 15 секунд перед запуском
while True:
    while hx < 10:
        ret, image = camera.read()  # Считываем кадр с камеры
        if not ret:  # Проверяем, удалось ли получить кадр
            print("Ошибка: Не удалось получить изображение.")
            break

        image = cv2.resize(image, (224, 224))  # Изменяем размер изображения
        image = np.asarray(image, dtype=np.float32) / 127.5 - 1 
        image = image.reshape(1, 224, 224, 3)  \


        prediction = model.predict(image)  # Делаем предсказание
        index = np.argmax(prediction)  # Находим индекс класса
        predicted_class = class_names[index][2:]  # Получаем название класса
        confidence_score = np.round(prediction[0][index] * 100, 2)  # Рассчитываем уверенность

        if confidence_score > 90:  # Если уверенность больше 90%
            print(f"Класс: {predicted_class}, Уверенность: {confidence_score}%")
    

        image = (image + 1) * 127.5  # Обрабатываем изображение для отображения
        image = image.astype(np.uint8)
        image = image[0]

        
        hx += 1

        cv2.imshow("Webcam Image", image)  # Отображаем изображение
    hx = 0
    while hx < 2:
        ret, image = camera.read()  # Считываем кадр с камеры
        if not ret:  # Проверяем, удалось ли получить кадр
            print("Ошибка: Не удалось получить изображение.")
            break

        image = cv2.resize(image, (224, 224))  # Изменяем размер изображения
        image = np.asarray(image, dtype=np.float32) / 127.5 - 1 
        image = image.reshape(1, 224, 224, 3)  \

  
        prediction = model.predict(image)  # Делаем предсказание
        index = np.argmax(prediction)  # Находим индекс класса
        predicted_class = class_names[index][2:]  # Получаем название класса
        confidence_score = np.round(prediction[0][index] * 100, 2)  # Рассчитываем уверенность

        if confidence_score > 90:  # Если уверенность больше 90%
            print(f"Класс: {predicted_class}, Уверенность: {confidence_score}%")
            if predicted_class == 'plastic\n':
                print(222)
                ser.write(struct.pack('f', d))
                # Отправляем команду 15 на Arduino
            else:  # Если класс не "paper"
                print(111)
 # Отправляем команду 10 на Arduino
            time.sleep(1)  # Ждем 1 секунды

        image = (image + 1) * 127.5  # Обрабатываем изображение для отображения
        image = image.astype(np.uint8)
        image = image[0]

        cv2.imshow("Webcam Image", image)  # Отображаем изображение
        if cv2.waitKey(1) == 27:  # Если нажата "Esc"
            break
    hx = 0
camera.release()  # Закрываем камеру
cv2.destroyAllWindows()  # Закрываем окна
ser.close()  # Закрываем подключение к Arduino
