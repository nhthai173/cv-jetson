import RPi.GPIO as GPIO

class DCMotor:
    def __init__(self, pinA, pinB):
        self.pinA = pinA
        self.pinB = pinB
        self.active_pin = None
        self.setup()
        self.stop()

    def setup(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pinA, GPIO.OUT)
        GPIO.setup(self.pinB, GPIO.OUT)

    def start(self):
        GPIO.output(self.pinA, GPIO.HIGH)
        GPIO.output(self.pinB, GPIO.LOW)
        self.active_pin = self.pinA

    def stop(self):
        GPIO.output(self.pinA, GPIO.LOW)
        GPIO.output(self.pinB, GPIO.LOW)
        self.active_pin = None

    def forward(self):
        GPIO.output(self.pinA, GPIO.HIGH)
        GPIO.output(self.pinB, GPIO.LOW)
        self.active_pin = self.pinA

    def backward(self):
        GPIO.output(self.pinA, GPIO.LOW)
        GPIO.output(self.pinB, GPIO.HIGH)
        self.active_pin = self.pinB

    def reverse(self):
        if self.active_pin == self.pinA:
            GPIO.output(self.pinA, GPIO.LOW)
            GPIO.output(self.pinB, GPIO.HIGH)
            self.active_pin = self.pinB
        elif self.active_pin == self.pinB:
            GPIO.output(self.pinA, GPIO.HIGH)
            GPIO.output(self.pinB, GPIO.LOW)
            self.active_pin = self.pinA
