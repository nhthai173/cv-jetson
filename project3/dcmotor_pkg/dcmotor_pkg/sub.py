import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from dcmotor_pkg.DCMotor import DCMotor
import time
import json

class DCMotorSubscriber(Node, DCMotor):
    def __init__(self, pinIN1, pinIN2, pinIN3, pinIN4):
        super().__init__('dcmotor_subscriber')
        self.m1 = DCMotor(pinIN1, pinIN2)
        self.m2 = DCMotor(pinIN3, pinIN4)
        self.subscription = self.create_subscription(String, 'dcmotor_control', self.control_motor, 10)
    
    def control_motor(self, msg):
        jdata = json.loads(msg.data)
        m1_control = jdata.get('m1')
        m2_control = jdata.get('m2')
        if m1_control:
            if m1_control == 'forward':
                self.get_logger().info('M1 Forward')
                self.m1.forward()
            elif m1_control == 'backward':
                self.get_logger().info('M1 Backward')
                self.m1.backward()
            elif m1_control == 'stop':
                self.get_logger().info('M1 Stop')
                self.m1.stop()
        if m2_control:
            if m2_control == 'forward':
                self.get_logger().info('M2 Forward')
                self.m2.forward()
            elif m2_control == 'backward':
                self.get_logger().info('M2 Backward')
                self.m2.backward()
            elif m2_control == 'stop':
                self.get_logger().info('M2 Stop')
                self.m2.stop()
    
    def destroy_node(self):
        self.m1.stop()
        self.m2.stop()
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    dcmotor_subscriber = DCMotorSubscriber(7, 11, 12, 13)
    
    # Test code
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