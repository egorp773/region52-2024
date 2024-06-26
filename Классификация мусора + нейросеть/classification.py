import tensorflow as tf
from tensorflow.keras.models import load_model
import cv2
import numpy as np
import time
import serial

# Load the model and labels
model = load_model("keras_Model.h5", compile=False)
class_names = open("labels.txt", "r").readlines()
url = 'http://172.20.10.11/'
# Настройка порта Arduino
ser = serial.Serial('COM3', 9600)
bbcd = 10
# Open the webcam
camera = cv2.VideoCapture(url)

time.sleep(15)
while True:
    # Capture image from webcam
    ret, image = camera.read()
    if not ret:  # Check if image capture was successful
        print("Error: Could not capture image from webcam.")
        break

    # Resize image
    image = cv2.resize(image, (224, 224))

    # Preprocess image
    image = np.asarray(image, dtype=np.float32) / 127.5 - 1
    image = image.reshape(1, 224, 224, 3)
    time.sleep(2)
    # Predict class
    prediction = model.predict(image)
    index = np.argmax(prediction)
    predicted_class = class_names[index][2:]
    confidence_score = np.round(prediction[0][index] * 100, 2)

    if confidence_score > 90:
        print(f"Class: {predicted_class}, Confidence: {confidence_score}%")
        # # Send the command once before the if-else

        if predicted_class == 'paper\n':  # Отправка 10 для пластика
            print(11111)
            ser.write(f"{15}\n".encode())
            print(33333) 
        else:
            print(22222)
            ser.write(f"{10}\n".encode())
        time.sleep(2)

    # Обработка для отображения изображения:
    image = (image + 1) * 127.5
    image = image.astype(np.uint8)
    image = image[0]

    # Display image
    cv2.imshow("Webcam Image", image)
    if cv2.waitKey(1) == 27:
        break

    # Exit on 'Esc' key
camera.release()
cv2.destroyAllWindows()
ser.close()
