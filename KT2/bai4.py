from time import sleep
from JETSON.RARM import RARM
import cv2
from ultralytics import YOLO

model = YOLO("best.pt")
cap = cv2.VideoCapture(0)
channels = ['9', '12', '17', '21', '24', '28']
arm = RARM(channel=channels)


def returnHome():
    arm.setPos([1765, 2214, 1520, 2133, 1482, 1765])
    sleep(1e-1)

def pos1():
    arm.setPos([1520, 2255, 745, 2010, 1480, 1600])
    sleep(1e-1)

def pos2():
    arm.setPos([2050, 2050, 1153, 2133, 1480, 1357])
    sleep(1e-1)

def pos3():
    arm.setPos([1031, 1806, 1398, 2133, 1480, 1888])
    sleep(1e-1)

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
                returnHome()
            elif "Hinh_tron_vang" in names and "So_2" in names:
                pos1()
            elif "Hinh_tron_vang" in names and "Chu_d" in names:
                pos2()
            elif "So_2" in names and "Chu_d" in names:
                pos3()
            elif "Hinh_tron_vang" in names:
                pos1()
            elif "So_2" in names:
                pos2()
            elif "Chu_d" in names:
                pos3()
            else:
                returnHome()

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        except:
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()
