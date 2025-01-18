import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import time
import json

class DCMotorPublisher(Node):
    def __init__(self):
        super().__init__('DCMotor_publisher')
        self.publisher_ = self.create_publisher(String, 'dcmotor_control', 10)

    def run(self):
        while rclpy.ok():
            input_value = input("""Nhấn F động cơ quay thuận\nNhấn R động cơ quay nghịch\nNhấn S động cơ dừng\nMời chọn: """)
            if input_value == 'F' or input_value == 'R' or input_value == 'S':
                if input_value == 'F':
                    input_value = 'forward'
                elif input_value == 'R':
                    input_value = 'backward'
                elif input_value == 'S':
                    input_value = 'stop'
            else:
                self.get_logger().info(f'Không hợp lệ: "{input_value}"')
                continue
            
            msg = String()
            msg.data = json.dumps({'m1': input_value, 'm2': input_value})
            self.publisher_.publish(msg)
            self.get_logger().info(f'Đã gửi: "{input_value}"')

    def destroy_node(self):
        msg = String()
        msg.data = json.dumps({'m1': 'stop', 'm2': 'stop'})
        self.publisher_.publish(msg)
        self.get_logger().info(f'Sending: {msg.data}')
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    node = DCMotorPublisher()

    try:
        node.run()
    except KeyboardInterrupt:
        node.get_logger().info('Stopped')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()