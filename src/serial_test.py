import serial
from time import sleep
from servo import SG90
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

pan_servo = SG90(P=0.15, I=0, D=0)
tilt_servo = SG90(P=0.1, I=0, D=0)