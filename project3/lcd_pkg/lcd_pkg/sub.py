import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from RPi_GPIO_i2c_LCD import lcd
import time
import json

class DCMotorSubscriber(Node, lcd):
    def __init__(self, i2c_addr):
        super().__init__('lcd_subscriber')
        self.lcd = lcd(i2c_addr)
        self.subscription = self.create_subscription(String, 'lcd_control', self.control_lcd, 10)
    
    def control_lcd(self, msg):
        str = msg.data
        strs = str.split('\n')
        for i in range(4):
            if strs[i]:
                self.lcd.set(strs[i], i+1)
                time.sleep(1e-3)
    
    def destroy_node(self):
        self.lcd.clear()
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    dcmotor_subscriber = DCMotorSubscriber(7, 11, 12, 13)
    
    # while True:
    #     try:
    #         dcmotor_subscriber.m1.forward()
    #         dcmotor_subscriber.m2.forward()
    #         time.sleep(4)
    #         dcmotor_subscriber.m1.backward()
    #         dcmotor_subscriber.m2.backward()
    #         time.sleep(4)
    #     except Exception as e:
    #         dcmotor_subscriber.get_logger().error(str(e))
    #         break
    #     except KeyboardInterrupt:
    #         dcmotor_subscriber.get_logger().info('Shutting down')
    #         dcmotor_subscriber.destroy_node()
    #         break
    
    rclpy.spin(dcmotor_subscriber)
    dcmotor_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()