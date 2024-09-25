from serial import Serial, PARITY_NONE, STOPBITS_ONE, EIGHTBITS
import numpy

class RARM:
    def __init__(self, port='/dev/ttyACM0', channel = ['9', '12', '17', '21', '24', '28']):
        """Initialize 6 DoF Robot arm

        Args:
            port (str, optional): Defaults to '/dev/ttyACM0' for jetson(ubuntu) or 'COMx' for windows.
            channel (list, optional): Defaults to ['9', '12', '17', '21', '24', '28'].
        """
        self.port = port
        self.channel = channel
        self.serial = Serial(port = self.port, baudrate = 115200, parity = PARITY_NONE, stopbits = STOPBITS_ONE, bytesize = EIGHTBITS, timeout = 1)
    def setPos(self, pos):
        buf = ''
        for i in range(len(pos)):
            buf += f'#{self.channel[i]}P{pos[i]}'
        buf+= 'T500D500\r\n'
        self.serial.write(buf.encode())
    def searchPoint(self):
        pass