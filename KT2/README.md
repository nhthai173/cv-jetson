# KT2

## Bài 1

- Cài đặt hệ điều hành
- [Cài đặt thư viện cần thiết](#cài-đặt-các-thư-viện-cần-thiết-cho-kt2)
- Nhận dạng được đối tượng

## Bài 2

- Nhận diện đối tượng kết hợp với điều khiển LED và động cơ

- [Code](./bai2.py)

## Bài 3

- Nhận diện đối tượng và hiển thị lên LCD

- [Code](./bai3.py)

## Bài 4

- Nhận diện đối tượng kết hợp với điều khiển cánh tay máy
- [Code](./bai4.py)
- Lưu ý: Phải chạy file bằng quyền sudo vì giao tiếp UART yêu cầu quyền sudo

```python3
sudo python3 bai4.py
```

## Tổng hợp
- Kết hợp bài 2, 3, 4 trong một file code

- Code: [all.py](./all.py)

- Lưu ý: Phải chạy file bằng quyền sudo vì giao tiếp UART yêu cầu quyền sudo

```python3
sudo python3 bai4.py
```

---

# Hướng dẫn sử dụng package JETSON

## 1. Sử dụng package RARM

Dùng để điều khiển cánh tay máy

![1727222014376](image/README/1727222014376.png)

> Để folder cùng cấp với file `arm.py` (đổi tên khác cũng được)

```python
# khai báo package dấn tới file RARM.py
from JETSON.RARM import RARM

# khai báo các channel từ khâu nối giá tới điểm cuối chấp hành
channels = ['9', '12', '17', '21', '24', '28']

arm = RARM(channels, port = 'COM13') 
# COM13 là cổng kết nối với ARM bằng máy tính Windows
# Nếu dùng trên Jetson thì không cần chỉ định. Mặc định là '/dev/ttyACM0'

# Khai báo trong jetson
# arm = RARM(channels)

while True:
    # đặt vị trí từ khâu nối giá tới điểm chấp hành cuối
    arm.setPos([1765, 2214, 1520, 2133, 1482, 1765])
    sleep(2)
    arm.setPos([2050, 2050, 1153, 2133, 1480, 1357])
    sleep(2)
    arm.setPos([1520, 2255, 745, 2010, 1480, 1600])
    sleep(2)
    arm.setPos([1031, 1806, 1398, 2133, 1480, 1888])
    sleep(2)
```

## 2. Sử dụng package DCMotor

Dùng để điều khiển động cơ bằng module L298N

Ví dụ:

```python
from JETSON.DCMotor import DCMotor
from time import sleep

# Khai báo động cơ 1
m1 = DCMotor(7, 11) # 7 và 11 là 2 chân điều khiển channel A
# Khai báo động cơ 2
m2 = DCMotor(12, 13) # 12 và 13 là 2 chân điều khiển channel B

while True:
    try:
        # quay thuận
        m1.forward()
        m2.forward()
        sleep(5)

        # dừng
        m1.stop()
        m2.stop()
        
        # quay nghịch
        m1.backward()
        m2.backward()
    except:
        break

# Dừng chương trình thì giải phóng các chân GPIO
GPIO.cleanup()
```

---

# Cài đặt các thư viện cần thiết cho KT2

> Nên cài đặt các thư viện ở quyền sudo

## 1. Cài đặt pip3

```bash
sudo apt install python3-pip
```
## 2. Cài đặt thư viện LCD

Để điều khiển LCD

```bash
sudo pip3 install RPi-GPIO-I2C-LCD
```

## 3. Cài đặt thư viện serial

Để điều khiển cánh tay máy

```bash
sudo pip3 install pyserial
```

## 4. Cài đặt ultralytics

Để chạy nhận diện

```bash
sudo pip3 install ultralytics
```

---

# Lỗi hay gặp và cách khắc phục

## 1. This module can only be run on a Raspberry Pi!

Trong code python, thay

```python
import RPi.GPIO as GPIO
```

thành

```python
import Jetson.GPIO as GPIO
```