'''
    Self-Driving RC Car Project

    File: webcam_detection.py
    Date: 12/1/17
    Author: Alfredo Salazar
    Version: 1.0

    A project to design a car that has a Raspberry Pi mounted
    on the top with a connected PiCamera. This camera will be
    used to detect stop signs, traffic lights, turns, etc.
'''
# Import libraries
import numpy as np
import cv2, urllib, time

# Define haar cascades
stop_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_stopsign.xml')

# Capture webcam
cap = cv2.VideoCapture(0)

# Create and resize window for detection
cv2.namedWindow('Webcam Detection', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Webcam Detection', 1200, 700)

# Create ranges for colors red, yellow, and green
lower_r = np.array([0, 0, 90], dtype = "uint8")
upper_r = np.array([36, 33, 255], dtype = "uint8")
lower_y = np.array([0, 128, 128], dtype = "uint8")
upper_y = np.array([62, 255, 255], dtype = "uint8")
lower_g = np.array([0, 80, 0], dtype = "uint8")
upper_g = np.array([100, 255, 127], dtype = "uint8")

while True:
    ret, img = cap.read()
    
    # Check if there's no frame
    if img is None:
        break

    # Find red in frame and apply mask
    mask_r = cv2.inRange(img, lower_r, upper_r)
    output_r = cv2.bitwise_and(img, img, mask = mask_r)

    # Find yellow in frame and apply mask
    mask_y = cv2.inRange(img, lower_y, upper_y)
    output_y = cv2.bitwise_and(img, img, mask = mask_y)

    # Find green in frame and apply mask
    mask_g = cv2.inRange(img, lower_g, upper_g)
    output_g = cv2.bitwise_and(img, img, mask = mask_g)
    
    # Convert image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect multiple stop signs
    stops = stop_cascade.detectMultiScale(gray, 1.3, 5)

    # Draw orange rectangles around detected stop signs
    for (sx,sy,sw,sh) in stops:
        cv2.rectangle(img,(sx,sy),(sx+sw,sy+sh),(0,128,255),2)

    # Show color key
    cv2.putText(img, "Orange=Stop", (0, 30), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 255, 255))

    # Create array to display in window
    topArray = np.hstack([img, output_r])
    bottomArray = np.hstack([output_y, output_g])
    combArray = np.vstack([topArray, bottomArray])

    # Display frame/image to window
    cv2.imshow('Webcam Detection',combArray)

    # Wait 1 ms for keypress
    k = cv2.waitKey(1)

    # Check if escape key is pressed
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
