import serial
from servo import SG90
from time import sleep
import cv2
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
pan_servo = SG90(P=-0.03, I=0.0, D=-0.035, angle=93)
tilt_servo = SG90(P=0.01, I=0.0, D=0.015, angle=80)

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)


while True:
    _, img = cap.read()
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Detect the faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    pan_servo.error = 0
    tilt_servo.error = 0
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        cv2.rectangle(img, (x + int(w/2) + 2, y + int(h/2) + 2), (x + int(w/2) - 2, y + int(h/2) - 2), (0, 0, 255), -1)
        cv2.rectangle(img, (305, 225), (335, 255), (0, 255, 0), 2)
        pan_servo.error = x + w/2 - 320
        tilt_servo.error = y + h/2 - 240
        break
    if pan_servo.error > 16:
        pan_servo.angle += -0.1
        pan_angle = str(pan_servo.angle) + "x!"
        serialInst.write(pan_angle.encode('utf-8'))
    if pan_servo.error < -16:
        pan_servo.angle += 0.1
        pan_angle = str(pan_servo.angle) + "x!"
        serialInst.write(pan_angle.encode('utf-8'))
    if tilt_servo.error > 12:
        tilt_servo.angle += 0.1
        tilt_angle = str(tilt_servo.angle) + "y!"
        serialInst.write(tilt_angle.encode('utf-8'))
    if tilt_servo.error < -12:
        tilt_servo.angle += -0.1
        tilt_angle = str(tilt_servo.angle) + "y!"
        serialInst.write(tilt_angle.encode('utf-8'))

    cv2.imshow('img', img)
    print(f"x: {pan_servo.error}, y: {tilt_servo.error}")
    # Stop if escape key is pressed
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
serialInst.close()
cap.release()
cv2.destroyAllWindows()