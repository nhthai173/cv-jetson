import cv2
import numpy as np
from ultralytics import YOLO
from RPi_GPIO_i2c_LCD import lcd # type: ignore
from JETSON import DCMotor
import RPi.GPIO as GPIO # type: ignore
from time import sleep

distance_gain = 1.0 # hệ số chuyển đổi từ px sang mm

i2c_address = 0x3f
lcdDisplay = lcd.HD44780(i2c_address)

m1 = DCMotor(7, 11)
m2 = DCMotor(12, 13)

all_pins = [15, 16, 18, 19, 21, 22, 23, 24] # 8 chân LED
GPIO.setmode(GPIO.BOARD)
for i in range(len(all_pins)):
    GPIO.setup(all_pins[i], GPIO.OUT, initial=GPIO.HIGH)

def iowrite(num: int, value = 1):
    GPIO.output(all_pins[num], GPIO.LOW if value == 1 else GPIO.HIGH)

def draw_object(image, name, object_center, container_mask, color=(0, 0, 255), unit='px'):
    """
    Vẽ đối tượng và hiển thị khoảng cách từ tâm đối tượng đến biên trên và biên dưới của băng tải

    Parameters:
    - image (numpy.ndarray): Ảnh đầu vào để vẽ đối tượng.
    - name (str): Tên của đối tượng.
    - object_center (tuple): Tọa độ (x, y) của tâm đối tượng.
    - container_mask (numpy.ndarray): Mặt nạ của container để xác định các cạnh.
    - color (tuple): Màu sắc để vẽ đối tượng, mặc định là màu đỏ (BGR format).
    - unit (str): Đơn vị của khoảng cách, mặc định là 'px' (pixel).

    Returns:
    - tuple: Khoảng cách từ tâm đối tượng đến cạnh trên và cạnh dưới của container.
      - distance_to_top_edge (float): Khoảng cách đến cạnh trên.
      - distance_to_bottom_edge (float): Khoảng cách đến cạnh dưới.
    """

    x_center, y_center = object_center
    img_height = container_mask.shape[0]

    # Kẻ đường thẳng qua tâm
    vertical_line = container_mask[:, x_center]

    # Giao điểm với biên trên và biên dưới
    y_top_edge = np.argmax(vertical_line > 0)
    y_bottom_edge = img_height - np.argmax(np.flipud(vertical_line) > 0)

    distance_to_top_edge = y_center - y_top_edge
    distance_to_bottom_edge = y_bottom_edge - y_center

    if unit == 'mm':
        distance_to_top_edge = transform_distance(distance_to_top_edge)
        distance_to_bottom_edge = transform_distance(distance_to_bottom_edge)

    # ===== hiển thị ======

    # hiện tên
    cv2.putText(image, name, (x_center - 50, y_center), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
    # vẽ tâm
    cv2.circle(image, (x_center, y_center), 5, (255, 0, 0), -1)
    # hiện tọa độ tâm
    cv2.putText(image, f'C: ({x_center}, {y_center})', (x_center + 20, y_center), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    # Vẽ đường thẳng khoảng cách
    thickness = 2
    cv2.line(image, (x_center, y_center), (x_center, y_top_edge), color, thickness)
    cv2.line(image, (x_center, y_center), (x_center, y_bottom_edge), color, thickness)

    # Hiển thị khoảng cách
    cv2.putText(image, f'T: {distance_to_top_edge:.1f}{unit}', (x_center + 20, int((y_center + y_top_edge) / 2)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
    cv2.putText(image, f'B: {distance_to_bottom_edge:.1f}{unit}', (x_center + 20, int((y_center + y_bottom_edge) / 2)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    return distance_to_top_edge, distance_to_bottom_edge


def mask_offset(mask, offset):
    """
    Dịch chuyển mặt nạ theo offset.
    """
    offset_x, offset_y = offset
    mask = np.roll(mask, offset_x, axis=1)
    mask = np.roll(mask, offset_y, axis=0)
    return mask

def draw_contours(image, mask, color=(0, 255, 0), fill=False):
    """
    Vẽ viền của mặt nạ lên ảnh.
    """
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(image, contours, 0, color, 2)
    if fill:
        overlay = image.copy()
        cv2.fillPoly(overlay, contours, color)
        opacity = 0.5
        cv2.addWeighted(overlay, opacity, image, 1 - opacity, 0, image)


def calc_distance(pt1, pt2):
    """
    Tính khoảng cách giữa 2 điểm.
    """
    x1, y1 = pt1
    x2, y2 = pt2
    return np.sqrt((x2 - x1) **2 + (y2 - y1) **2)


def display_bangtai_size(mask, image, display=True):
    # Tìm 4 góc của băng tải
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    points = []
    if contours:
        cnt = contours[0]
        epsilon = 0.02 * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)
        for point in approx:
            x, y = point[0]
            points.append((x, y))
    # Vẽ cạnh
    if len(points) == 4:
        d1 = calc_distance(points[0], points[1])
        d2 = calc_distance(points[1], points[2])
        d3 = calc_distance(points[2], points[3])
        d4 = calc_distance(points[3], points[0])
        if display:
            cv2.line(image, points[0], points[1], (255, 0, 0), 2, -1)
            cv2.line(image, points[1], points[2], (255, 0, 0), 2, -1)
            cv2.line(image, points[2], points[3], (255, 0, 0), 2, -1)
            cv2.line(image, points[3], points[0], (255, 0, 0), 2, -1)
            cv2.putText(image, f'{d1:.1f}px d1', (int((points[0][0] + points[1][0]) / 2), int((points[0][1] + points[1][1]) / 2)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
            cv2.putText(image, f'{d2:.1f}px d2', (int((points[1][0] + points[2][0]) / 2), int((points[1][1] + points[2][1]) / 2)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
            cv2.putText(image, f'{d3:.1f}px d3', (int((points[2][0] + points[3][0]) / 2), int((points[2][1] + points[3][1]) / 2)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
            cv2.putText(image, f'{d4:.1f}px d4', (int((points[3][0] + points[0][0]) / 2), int((points[3][1] + points[0][1]) / 2)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
        return d1, d2, d3, d4
    return None

def calibrate_distance(container_width):
    """
    Calibrate hệ số chuyển đổi từ px sang mm.
    """
    real_width = 55
    global distance_gain
    distance_gain = real_width / container_width

def transform_distance(distance):
    """
    Transform the distance from pixels to a mm.
    """
    return distance * distance_gain

def display_lcd(object, cX, cY, top_distance, bottom_distance):
    """
    Hiển thị LCD, điều khiển động cơ và LED.
    """

    lcdDisplay.clear()
    sleep(1e-1)
    if object is None:
        lcdDisplay.set("No object", 1)
        for i in range(len(all_pins)):
            iowrite(i, 0)
        m1.stop()
        m2.stop()
        return
    
    lcdDisplay.set(f'N: {object}', 1)
    lcdDisplay.set(f'T: {top_distance}px', 2)
    lcdDisplay.set(f'C: ({cX}, {cY})', 3)
    lcdDisplay.set(f'B: {bottom_distance}px', 4)
    sleep(1e-1)

    if top_distance >= 50:
        m1.forward()
        iowrite(7, 1)
        iowrite(6, 1)
        iowrite(5, 1)
        iowrite(4, 1)
    elif top_distance >= 40:
        m1.stop()
        iowrite(7, 1)
        iowrite(6, 1)
        iowrite(5, 1)
        iowrite(4, 0)
    else:
        m1.stop()
        iowrite(7, 0)
        iowrite(6, 0)
        iowrite(5, 0)
        iowrite(4, 0)
        
    if bottom_distance >= 50:
        m2.forward()
        iowrite(0, 1)
        iowrite(1, 1)
        iowrite(2, 1)
        iowrite(3, 1)
    elif bottom_distance >= 40:
        m2.stop()
        iowrite(0, 1)
        iowrite(1, 1)
        iowrite(2, 1)
        iowrite(3, 0)
    else:
        m2.stop()
        iowrite(0, 0)
        iowrite(1, 0)
        iowrite(2, 0)
        iowrite(3, 0)


# Load the YOLOv8 model
model = YOLO('./best.pt')

cap = cv2.VideoCapture(0)

COLORS = {
    'Bangtai': (35, 73, 42),
    'Xanh': (134, 176, 102),
    'Do': (54, 71, 188),
    'Trang': (255, 255, 255),
}

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        continue

    original_height, original_width = frame.shape[:2]
    results = model(frame, conf=0.5, verbose=False)
    annotated_frame = frame.copy()

    names = []
    result = results[0]
    container_mask = None
    objects = []

    if result.masks and result.boxes:
        for i in range(len(result.boxes.data)):
            box_data = result.boxes.data[i]
            box = result.boxes[i]
            mask = result.masks.data[i]
            m = mask.cpu().numpy().astype(np.uint8)
            m = cv2.resize(m, (original_width, original_height), interpolation=cv2.INTER_LINEAR_EXACT)
            m = mask_offset(m, (0, 0))
            class_id = int(box.cls)
            object_data = {}
            object_data['name'] = model.names[class_id]
            object_data['mask'] = m
            color = COLORS.get(object_data['name'], (0, 255, 0))

            # Băng tải
            if object_data['name'] == 'Bangtai':
                container_mask = m
                draw_contours(annotated_frame, m, (0, 255, 0), False)

            # Các đối tượng khác
            else:
                # Vẽ mask
                draw_contours(annotated_frame, m, color, True)

                # Tìm tâm theo contour
                contours, _ = cv2.findContours(
                    m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                if contours:
                    M = cv2.moments(contours[0])
                    if M['m00'] != 0:
                        cX = int(M['m10'] / M['m00'])
                        cY = int(M['m01'] / M['m00'])
                        object_data['center'] = (cX, cY)

                objects.append(object_data)

    if container_mask is not None:
        distances = display_bangtai_size(container_mask, annotated_frame, display=False)
        if distances:
            # Tính hệ số chuyển đổi
            d1, d2, d3, d4 = distances
            calibrate_distance(max(d2, d4))

    # Tính khoảng cách
    for object in objects:
        if 'center' in object and container_mask is not None: 
            top, bottom = draw_object(annotated_frame, object['name'], object['center'], container_mask, color=(188, 223, 235))
            cX, cY = object['center']
            display_lcd(object['name'], cX, cY, top, bottom)
            break # chỉ hiển thị 1 đối tượng
    if not objects or len(objects) == 0:
        display_lcd(None, None, None, None, None)

    cv2.imshow('frame', annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
GPIO.cleanup()