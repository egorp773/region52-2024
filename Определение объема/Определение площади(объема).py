import numpy as np
import cv2
import imutils
import serial
import struct
import time

url = 'http://172.20.10.3:8080/video'  # Замените на URL вашей камеры
number = 1
print(1)



ser = serial.Serial('COM7', 9600)  # Replace with your serial port
# Set video resolution (optional

# Initialize variables
area = 0
mx = 0
xq = 0
k = 0
# Define the region of interest (ROI) coordinates
x1 = 620 # Левая координата ROI
y1 = 120 # 70Верхняя координата ROI
x2 = 920 # Правая координата ROI
y2 = 625 # Нижняя координата ROI8
print(20)
while k!= 10:
    data = ser.readline().decode('ascii').strip()
    if data:
        number = int(data)
        print(123213213)
        k = 10
# Initialize serial communication
cap = cv2.VideoCapture(url)
cap.set(3, 300)
cap.set(4, 480)
time.sleep(1)  # Wait for serial port to be ready

while xq < 10:
    # Capture frame-by-frame
    ret, frame = cap.read()

    if not ret:
        print("Error: Failed to capture frame")
        break

    # Extract the ROI from the frame
    roi = frame[y1:y2, x1:x2]

    # Convert the ROI to HSV color space
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    # Define the lower and upper bounds for white color (adjust these values as needed)
    lower_white = np.array([0, 0, 150])  # Adjust the lower bound for less brightness
    upper_white = np.array([180, 30, 255])

    # Threshold the HSV image to get only white colors
    mask = cv2.inRange(hsv, lower_white, upper_white)

    # Find contours in the thresholded image
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    # Loop over the contours
    for c in cnts:
        # Calculate area of the contour
        area = cv2.contourArea(c)

        # Ignore small contours
        if area > 100:  # Adjust this threshold as needed
            # Draw contour outline on the ROI
            cv2.drawContours(roi, [c], -1, (0, 255, 0), 2)

            # Calculate centroid of the contour
            M = cv2.moments(c)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
            else:
                cx, cy = 0, 0

            # Draw centroid on the ROI
            cv2.circle(roi, (cx, cy), 5, (255, 255, 255), -1)
            cv2.putText(roi, "Center", (cx - 20, cy - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Display the resulting frame (with ROI highlighted)
    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Draw ROI rectangle
    cv2.imshow('Webcam', frame)

    # Update maximum area
    if area > mx:
        mx = area
        print("Area:", mx)
        mx = mx/1
    # Send data to Arduino
    float_var = mx
    ser.write(struct.pack('f', float_var))
      # Wait for Arduino to process data
    print(float_var)
    # Wait for 1 second


    # Increment loop counter
    xq += 1
xq = 0 
while xq < 50:
    # Capture frame-by-frame
    ret, frame = cap.read()

    if not ret:
        print("Error: Failed to capture frame")
        break

    # Extract the ROI from the frame
    roi = frame[y1:y2, x1:x2]

    # Convert the ROI to HSV color space
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    # Define the lower and upper bounds for white color (adjust these values as needed)
    lower_white = np.array([0, 0, 150])  # Adjust the lower bound for less brightness
    upper_white = np.array([180, 30, 255])

    # Threshold the HSV image to get only white colors
    mask = cv2.inRange(hsv, lower_white, upper_white)

    # Find contours in the thresholded image
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    # Loop over the contours
    for c in cnts:
        # Calculate area of the contour
        area = cv2.contourArea(c)

        # Ignore small contours
        if area > 100:  # Adjust this threshold as needed
            # Draw contour outline on the ROI
            cv2.drawContours(roi, [c], -1, (0, 255, 0), 2)

            # Calculate centroid of the contour
            M = cv2.moments(c)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
            else:
                cx, cy = 0, 0

            # Draw centroid on the ROI
            cv2.circle(roi, (cx, cy), 5, (255, 255, 255), -1)
            cv2.putText(roi, "Center", (cx - 20, cy - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Display the resulting frame (with ROI highlighted)
    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Draw ROI rectangle
    cv2.imshow('Webcam', frame)

    # Update maximum area
    if area > mx:
        mx = area
        print("Area:", mx)
        mx = mx/1
    # Send data to Arduino
    float_var = mx
    ser.write(struct.pack('f', float_var))
    time.sleep(1)  # Wait for Arduino to process data

    # Wait for 1 second
    time.sleep(1)

    # Increment loop counter
    xq += 1

    # Check for key press; if 'q' is pressed, exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Close serial port connection
ser.close()

# Release the video capture object and close all windows
cap.release()
cv2.destroyAllWindows()
