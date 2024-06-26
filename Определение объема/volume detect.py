import numpy as np
import cv2
import imutils
import serial
import struct
import time

# Read input video stream from an IP camera
url = "http://192.168.34.201:4747/video"  # Replace with your IP camera URL
cap = cv2.VideoCapture(url)

# Set video resolution x(optional)
cap.set(3, 300)
cap.set(4, 480)

# Initialize variables
area = 0
mx = 0
xq = 0

# Initialize serial communication
ser = serial.Serial('/dev/cu.usbserial-1420', 9600)  # Replace with your serial port
time.sleep(1)  # Wait for serial port to be ready

while xq < 50:
    # Capture frame-by-frame
    ret, frame = cap.read()

    if not ret:
        print("Error: Failed to capture frame")
        break

    # Convert the frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define the lower and upper bounds for blue color
    lower_blue = np.array([0, 0, 200])
    upper_blue = np.array([180, 30, 255])

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Find contours in the thresholded image
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    # Loop over the contours
    for c in cnts:
        # Calculate area of the contour
        area = cv2.contourArea(c)

        # Ignore small contours
        if area > 100:  # Adjust this threshold as needed
            # Draw contour outline
            cv2.drawContours(frame, [c], -1, (0, 255, 0), 2)

            # Calculate centroid of the contour
            M = cv2.moments(c)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
            else:
                cx, cy = 0, 0

            # Draw centroid
            cv2.circle(frame, (cx, cy), 5, (255, 255, 255), -1)
            cv2.putText(frame, "Center", (cx - 20, cy - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow('Webcam', frame)

    # Update maximum area
    if area > mx:
        mx = area
    print("Area:", mx)

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
