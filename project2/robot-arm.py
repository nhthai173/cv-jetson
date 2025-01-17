import cv2
from ultralytics import YOLO
from JETSON import RARM
from time import sleep
from threading import Thread

channels = ['9', '12', '17', '25', '26', '28']
arm = RARM(channel=channels)
pos1, pos2, pos3 = 868, 1132, 1500
thing_p = {
    'trang': [1000, 1800],
    'do': [1000, 1800],
    'xanh': [940, 2100]
}

NAME = None
ARM_RUNNING = False

def goTo(arm: RARM, p1: int, p2: int, p3: int, time = 3000):
    pos = arm.lastPos
    pos[0] = p1
    pos[1] = p2
    pos[2] = p3
    if pos[-3] <= 0:
        pos[-3] = 900
    if pos[-2] <= 0:
        pos[-2] = 1500
    if pos[-1] <= 0:
        pos[-1] = 1000
    arm.setPos(pos, time)
    sleep(1)

def gap(arm: RARM, thing: str):
    if not thing_p.get(thing):
        return
    pos = arm.lastPos
    pos[-3] = thing_p[thing][0]
    arm.setPos(pos)
    pos[-1] = thing_p[thing][1]
    arm.setPos(pos)
    pos[-3] = thing_p[thing][0] - 100
    arm.setPos(pos)

def nha(arm: RARM, thing: str):
    pos = arm.lastPos
    pos[-3] = thing_p[thing][0]
    arm.setPos(pos)
    pos[-1] = 1000
    arm.setPos(pos)
    pos[-3] = 500
    arm.setPos(pos)

def home(arm: RARM):
    h = [2132, 1921, 605, 500, 1500, 1000]
    if not isHome(arm, h):
        arm.setPos(h, time=1000)
        sleep(1.5)

def gap_trang():
    goTo(arm, 2132, 1921, 605, time=1000)
    gap(arm, 'trang')
    goTo(arm, 868, 1921, 605)    
    nha(arm, 'trang')

def gap_do():
    goTo(arm, 2132, 1921, 605, time=1000)
    gap(arm, 'do')
    goTo(arm, 1132, 1921, 605)    
    nha(arm, 'do')

def gap_xanh():
    goTo(arm, 2132, 1921, 605, time=1000)
    gap(arm, 'xanh')
    goTo(arm, 1500, 1921, 605)    
    nha(arm, 'xanh')

def isHome(arm: RARM, hpos):
    return hpos == arm.lastPos

def arm_thread():
    while True:
        global NAME, ARM_RUNNING
        print(NAME)
        if ARM_RUNNING:
            continue
        name = NAME
        if not name:
            home(arm)
            continue

        ARM_RUNNING = True
        if name == 'Trang':
            gap_trang()
        if name == 'Do':
            gap_do()
        if name == 'Xanh':
            gap_xanh()
        NAME = None
        ARM_RUNNING = False

Thread(target=arm_thread).start()

model = YOLO("./best.pt")
cap = cv2.VideoCapture(0)

while True:
    success, frame = cap.read()
    if success:
        results = model(frame, conf=0.5)
        names = []
        
        if len(results) == 0:
            continue
        result = results[0]
        annotated_frame = result.plot()
        for box in result.boxes:
            class_id = int(box.cls)
            object_name = model.names[class_id]
            names.append({'name': object_name, 'conf': float(box.conf[0])})
        name = None
        if len(names):
            max_conf_entry = max(names, key=lambda x: x['conf'])
            name = max_conf_entry['name']
            NAME = name
                
        cv2.imshow("YOLO8 Interface", annotated_frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()