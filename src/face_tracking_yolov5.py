import serial
from servo import SG90
from time import sleep
import torch
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
pan_servo = SG90(P=0.01, I=0.0, D=0.0, angle=93)
tilt_servo = SG90(P=0.01, I=0.0, D=0.0, angle=93)

model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt', force_reload=True)

cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

SP_pan = 320
SP_tilt = 240

PV_pan_prev = 320
PV_tilt_prev = 240

while True:
    _, img = cap.read()

    results = model(img)
    image = cv2.rectangle(np.squeeze(results.render()), (305, 225), (335, 255), (0, 255, 0), 2)
    pan_servo.error = 0
    tilt_servo.error = 0

    PV_pan = 320
    PV_tilt = 240

    for index in range(results.pandas().xyxy[0].name.size):
        if results.pandas().xyxy[0].name[index] == 'face':
            PV_pan = int((results.pandas().xyxy[0].xmax[index] + results.pandas().xyxy[0].xmin[index]) / 2)
            PV_tilt = int((results.pandas().xyxy[0].ymax[index] + results.pandas().xyxy[0].ymin[index]) / 2)
            break

    pan_servo.error = SP_pan - PV_pan
    tilt_servo.error = SP_tilt - PV_tilt

    if abs(pan_servo.error) > 16:
        pan_servo.angle += pan_servo.P * pan_servo.error + pan_servo.I * pan_servo.sum_error + pan_servo.D * (
                    PV_pan_prev - PV_pan)  # (pan_servo.error - pan_servo.prev_error)
        pan_angle = str(pan_servo.angle) + "x!"
        serialInst.write(pan_angle.encode('utf-8'))
    if abs(tilt_servo.error) > 12:
        tilt_servo.angle += tilt_servo.P * tilt_servo.error + tilt_servo.I * tilt_servo.sum_error + tilt_servo.D * (
                    PV_tilt_prev - PV_tilt)
        tilt_angle = str(tilt_servo.angle) + "y!"
        serialInst.write(tilt_angle.encode('utf-8'))

    # pan_servo.prev_error = pan_servo.error
    PV_pan_prev = PV_pan
    pan_servo.sum_error += pan_servo.error

    # tilt_servo.prev_error = tilt_servo.error
    PV_tilt_prev = PV_tilt
    tilt_servo.sum_error += tilt_servo.error

    image = cv2.rectangle(image, (PV_pan + 2, PV_tilt + 2), (PV_pan - 2, PV_tilt - 2), (0, 0, 255), -1)

    cv2.imshow('img', image)
    print(f"x: {pan_servo.error}, y: {tilt_servo.error}")
    # Stop if escape key is pressed
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
serialInst.close()
cap.release()
cv2.destroyAllWindows()