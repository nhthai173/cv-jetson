from __future__ import print_function
from DCMotor import DCMotor
import cv2
from ultralytics import YOLO

import RPi.GPIO as GPIO # type: ignore

m1 = DCMotor(7, 11)
m2 = DCMotor(12, 13)
all_pins = [15, 16, 18, 19, 21, 22, 23, 24]
GPIO.setmode(GPIO.BOARD)

for i in range(len(all_pins)):
    GPIO.setup(all_pins[i], GPIO.OUT, initial=GPIO.HIGH)

def iowrite(num: int, value: int):
    GPIO.output(all_pins[num], GPIO.LOW if value == 1 else GPIO.HIGH)

def defaultIO():
    for i in range(len(all_pins)):
        iowrite(i, 0)
    m1.stop()
    m2.stop()

def cleanupGPIO():
    for i in range(len(all_pins)):
        GPIO.output(all_pins[i], GPIO.HIGH)
    GPIO.cleanup()

model = YOLO("best.pt")
cap = cv2.VideoCapture(0)
m1.stop()
m2.stop()
while True:
    success, frame = cap.read()
    if success:
        results = model(frame)
        names = []
        
        if len(results) == 0:
            continue
        result = results[0]
        annotated_frame = result.plot()
        for box in result.boxes:
            class_id = int(box.cls)
            object_name = model.names[class_id]
            names.append(object_name)
                
        cv2.imshow("YOLO8 Interface", annotated_frame)
        
        try:
            if "Hinh_tron_vang" in names and "So_2" in names and "Chu_d" in names:
                defaultIO()
                m1.forward()
                m2.forward()
                iowrite(6, 1)
            elif "Hinh_tron_vang" in names and "So_2" in names:
                defaultIO()
                m1.forward()
                m2.backward()
                iowrite(3, 1)
            elif "Hinh_tron_vang" in names and "Chu_d" in names:
                defaultIO()
                m1.backward()
                m2.forward()
                iowrite(4, 1)
            elif "So_2" in names and "Chu_d" in names:
                defaultIO()
                m2.backward()
                iowrite(5, 1)
            elif "Hinh_tron_vang" in names:
                defaultIO()
                m1.forward()
                iowrite(0, 1)
            elif "So_2" in names:
                defaultIO()
                m2.forward()
                iowrite(1, 1)
            elif "Chu_d" in names:
                defaultIO()
                m1.backward()
                iowrite(2, 1)
            else:
                defaultIO()
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        except:
            break
    else:
        break

GPIO.setmode(GPIO.BOARD)
m1.stop()
m2.stop()
cleanupGPIO()
cap.release()
cv2.destroyAllWindows()