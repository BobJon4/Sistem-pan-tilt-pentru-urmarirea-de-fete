import serial
from servo import SG90
from time import sleep
import cv2
import numpy as np
BAUD_RATE = 115200
PORT = "COM9"

# Initialise and open the serial port

serialInst = serial.Serial()
serialInst.baudrate = BAUD_RATE
serialInst.port = PORT
serialInst.open()
print(f"{PORT} has been open!")
sleep(0.5)

# Initialise servo control
K_u = 0.06 # 0.0701
T_u = 0.29
pan_servo = SG90(P=K_u * 0.2, I=0.4 * K_u / T_u * 0.01, D=0.066 * K_u * T_u / 0.1, angle=93)
tilt_servo = SG90(P=0.008, I=0.0, D=0.0, angle=93)

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

SP_pan = 320
SP_tilt = 240

PV_pan_prev = 320
PV_tilt_prev = 240

while True:
    _, img = cap.read()
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Detect the faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    pan_servo.error = 0
    tilt_servo.error = 0

    PV_pan = 320
    PV_tilt = 240

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        cv2.rectangle(img, (x + int(w/2) + 2, y + int(h/2) + 2), (x + int(w/2) - 2, y + int(h/2) - 2), (0, 0, 255), -1)
        cv2.rectangle(img, (305, 225), (335, 255), (0, 255, 0), 2)
        PV_pan = x + w/2
        PV_tilt = y + h/2
        # pan_servo.error = x + w/2 - 320
        # tilt_servo.error = y + h/2 - 240
        break

    pan_servo.error = SP_pan - PV_pan
    tilt_servo.error = SP_tilt - PV_tilt

    if abs(pan_servo.error) > 16:
        pan_servo.angle += pan_servo.P * pan_servo.error + pan_servo.I * pan_servo.sum_error + pan_servo.D * (PV_pan_prev - PV_pan) # (pan_servo.error - pan_servo.prev_error)
        pan_angle = str(pan_servo.angle) + "x!"
        serialInst.write(pan_angle.encode('utf-8'))
    if abs(tilt_servo.error) > 12:
        tilt_servo.angle += tilt_servo.P * tilt_servo.error + tilt_servo.I * tilt_servo.sum_error + tilt_servo.D * (PV_tilt_prev - PV_tilt)
        tilt_angle = str(tilt_servo.angle) + "y!"
        serialInst.write(tilt_angle.encode('utf-8'))

    # pan_servo.prev_error = pan_servo.error
    PV_pan_prev = PV_pan
    pan_servo.sum_error += pan_servo.error

    if pan_servo.sum_error > 10:
        pan_servo.sum_error = 10
    elif pan_servo.sum_error < -10:
        pan_servo.sum_error = -10

    # tilt_servo.prev_error = tilt_servo.error
    PV_tilt_prev = PV_tilt
    tilt_servo.sum_error += tilt_servo.error

    cv2.imshow('img', img)
    print(f"x: {pan_servo.error}, y: {tilt_servo.error}")
    # Stop if escape key is pressed
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
serialInst.close()
cap.release()
cv2.destroyAllWindows()


