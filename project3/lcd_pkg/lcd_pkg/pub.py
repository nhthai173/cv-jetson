import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import time
import json

class LCDPublisher(Node):
    def __init__(self):
        super().__init__('lcd_publisher')
        self.publisher_ = self.create_publisher(String, 'lcd_control', 10)
        # self.timer = self.create_timer(3.0, self.timer_callback)
        self.state = 0
    
    def run(self):
        msg = String()
        msg.data = 'Nguyen Huy Thai\nTran Thi Ngoc Hoa\nNguyen Son Phu'
        self.publisher_.publish(msg)

    def destroy_node(self):
        msg = String()
        msg.data = json.dumps({'m1': 'stop', 'm2': 'stop'})
        self.publisher_.publish(msg)
        self.get_logger().info(f'Sending: {msg.data}')
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    lcd_publisher = LCDPublisher()
    rclpy.spin(lcd_publisher)
    lcd_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()