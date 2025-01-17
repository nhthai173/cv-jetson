import cv2
from ultralytics import YOLO
from RPi_GPIO_i2c_LCD import lcd # type: ignore
from time import sleep

i2c_address = 0x3f

lcdDisplay = lcd.HD44780(i2c_address)

def dsp_center(dsp: lcd.HD44780, msg: str, line: int):
    dsp.set(msg.center(20), line)

def dsp_right(dsp: lcd.HD44780, msg: str, line: int):
    dsp.set(msg.rjust(20), line)

def dsp_left(dsp: lcd.HD44780, msg: str, line: int):
    dsp.set(msg.ljust(20), line)

def dsp_clear(dsp: lcd.HD44780):
    dsp.clear()
    sleep(1e-3)


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
            
            dsp_clear(lcdDisplay)
            for i in range(len(names)):
                dsp_left(lcdDisplay, names[i], i+1)
            sleep(1)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        except:
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()