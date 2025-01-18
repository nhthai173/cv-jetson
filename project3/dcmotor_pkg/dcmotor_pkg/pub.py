import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import time
import json

class DCMotorPublisher(Node):
    def __init__(self):
        super().__init__('DCMotor_publisher')
        self.publisher_ = self.create_publisher(String, 'dcmotor_control', 10)
        self.timer = self.create_timer(3.0, self.timer_callback)
        self.state = 0
    
    def timer_callback(self):
        self.state = (self.state + 1) % 3
        if self.state == 0:
            data_str = 'forward'
        elif self.state == 1:
            data_str = 'backward'
        elif self.state == 2:
            data_str = 'stop'

        msg = String()
        msg.data = json.dumps({'m1': data_str, 'm2': data_str})
        self.publisher_.publish(msg)
        self.get_logger().info(f'Sending: {msg.data}')

    def destroy_node(self):
        msg = String()
        msg.data = json.dumps({'m1': 'stop', 'm2': 'stop'})
        self.publisher_.publish(msg)
        self.get_logger().info(f'Sending: {msg.data}')
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    dcmotor_publisher = DCMotorPublisher()
    rclpy.spin(dcmotor_publisher)
    dcmotor_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()