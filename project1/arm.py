from time import sleep
from JETSON import RARM

channels = ['9', '12', '17', '21', '24', '28']
arm = RARM(port = 'COM13')

while 1:
    arm.setPos([1765, 2214, 1520, 2133, 1482, 1765])
    sleep(2)
    arm.setPos([2050, 2050, 1153, 2133, 1480, 1357])
    sleep(2)
    arm.setPos([1520, 2255, 745, 2010, 1480, 1600])
    sleep(2)
    arm.setPos([1031, 1806, 1398, 2133, 1480, 1888])
    sleep(2)