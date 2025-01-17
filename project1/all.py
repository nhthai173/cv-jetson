import cv2
from ultralytics import YOLO
from RPi_GPIO_i2c_LCD import lcd # type: ignore
from JETSON import RARM, DCMotor
import RPi.GPIO as GPIO # type: ignore
from time import sleep

i2c_address = 0x3f
lcdDisplay = lcd.HD44780(i2c_address)

channels = ['9', '12', '17', '21', '24', '28']
arm = RARM(channel=channels)

m1 = DCMotor(7, 11)
m2 = DCMotor(12, 13)

all_pins = [15, 16, 18, 19, 21, 22, 23, 24]
GPIO.setmode(GPIO.BOARD)

for i in range(len(all_pins)):
    GPIO.setup(all_pins[i], GPIO.OUT, initial=GPIO.HIGH)

def iowrite(num: int, value = 1):
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

def dsp_center(dsp: lcd.HD44780, msg: str, line: int):
    dsp.set(msg.center(20), line)

def dsp_right(dsp: lcd.HD44780, msg: str, line: int):
    dsp.set(msg.rjust(20), line)

def dsp_left(dsp: lcd.HD44780, msg: str, line: int):
    dsp.set(msg.ljust(20), line)

def dsp_clear(dsp: lcd.HD44780):
    dsp.clear()
    sleep(1e-3)


def returnHome():
    arm.setPos([1765, 2214, 1520, 2133, 1482, 1765])
    sleep(1e-1)

def pos1():
    arm.setPos([2050, 2050, 1153, 2133, 1480, 1357])
    sleep(1e-1)

def pos2():
    arm.setPos([1520, 2255, 745, 2010, 1480, 1600])
    sleep(1e-1)

def pos3():
    arm.setPos([1031, 1806, 1398, 2133, 1480, 1888])
    sleep(1e-1)


model = YOLO("best.pt")
cap = cv2.VideoCapture(0)
dsp_clear(lcdDisplay)

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
            # Dieu khien
            if "Hinh_tron_vang" in names and "So_2" in names and "Chu_d" in names:
                returnHome()
                defaultIO()
                m1.forward()
                m2.forward()
                iowrite(6)
            elif "Hinh_tron_vang" in names and "So_2" in names:
                pos1()
                defaultIO()
                m1.forward()
                m2.backward()
                iowrite(3)
            elif "Hinh_tron_vang" in names and "Chu_d" in names:
                pos2()
                defaultIO()
                m1.backward()
                m2.forward()
                iowrite(4)
            elif "So_2" in names and "Chu_d" in names:
                pos3()
                defaultIO()
                m2.backward()
                iowrite(5)
            elif "Hinh_tron_vang" in names:
                pos1()
                defaultIO()
                m1.forward()
                iowrite(0)
            elif "So_2" in names:
                pos2()
                defaultIO()
                m2.forward()
                iowrite(1)
            elif "Chu_d" in names:
                pos3()
                defaultIO()
                m1.backward()
                iowrite(2)
            else:
                returnHome()
                defaultIO()
                m1.stop()
                m2.stop()

            # Hien thi tren LCD
            dsp_clear(lcdDisplay)
            for i in range(len(names)):
                line = i+1
                if names[i] == 'Hinh_tron_vang':
                    dsp_center(lcdDisplay, names[i], line)
                elif names[i] == 'So_2':
                    dsp_right(lcdDisplay, names[i], line)
                elif names[i] == 'Chu_d':
                    dsp_left(lcdDisplay, names[i], line)
            sleep(1)

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