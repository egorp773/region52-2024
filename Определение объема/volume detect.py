import numpy as np
import cv2
import imutils
import serial
import struct
import time

# Чтение видеопотока с IP-камеры
url = "http://192.168.34.201:4747/video"  # URL IP-камеры
cap = cv2.VideoCapture(url)

# Установка разрешения видео (необязательно)
cap.set(3, 300)  # Ширина
cap.set(4, 480)  # Высота

# Инициализация переменных
area = 0
mx = 0  # Максимальная площадь
xq = 0  # Счетчик цикла

ser = serial.Serial('/dev/cu.usbserial-1420', 9600)  # Порт Arduino
time.sleep(1)  

while xq < 50:  # Цикл обработки кадров
    ret, frame = cap.read()  # Чтение кадра
    if not ret:
        print("Ошибка: Не удалось получить кадр")
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  
    lower_blue = np.array([0, 0, 200])  # Нижняя граница синего цвета
    upper_blue = np.array([180, 30, 255])  # Верхняя граница синего цвета
    mask = cv2.inRange(hsv, lower_blue, upper_blue)  # Маска для синего цвета

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # Нахождение контуров
    cnts = imutils.grab_contours(cnts)

    for c in cnts:  # Цикл по контурам
        area = cv2.contourArea(c)  # Расчет площади
        if area > 100:  # Фильтрация по площади
            cv2.drawContours(frame, [c], -1, (0, 255, 0), 2)  # Рисуем контур

            M = cv2.moments(c)  # Расчет центра масс
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
            else:
                cx, cy = 0, 0

            cv2.circle(frame, (cx, cy), 5, (255, 255, 255), -1)  # Рисуем центр
            cv2.putText(frame, "Center", (cx - 20, cy - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    cv2.imshow('Webcam', frame)  # Отображение кадра

    if area > mx:  # Обновление максимальной площади
        mx = area
        mx = mx/122.5 * 12
    print("Площадь:", mx)

    
    float_var = mx
    ser.write(struct.pack('f', float_var))  # Отправка данных
    time.sleep(1)  # Пауза для обработки данных

    xq += 1  # Увеличение счетчика цикла

    if cv2.waitKey(1) & 0xFF == ord('q'):  # Выход при нажатии "q"
        break

ser.close()  # Закрытие последовательного порта
cap.release()  # Освобождение видеозахвата
cv2.destroyAllWindows()  # Закрытие окон
