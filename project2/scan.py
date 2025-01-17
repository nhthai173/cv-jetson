import serial.tools.list_ports

def list_serial_ports():
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]

if __name__ == '__main__':
    print(list_serial_ports())
