import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image

import cv2
from cv_bridge import CvBridge

import os
os.environ['ROS_DOMAIN_ID'] = '1'
os.environ['RMW_IMPLEMENTATION'] = 'rmw_fastrtps_cpp'
os.environ['ROS_LOCALHOST_ONLY'] = '0'

class ImageSubscriber(Node):
    def __init__(self, name):
        super().__init__(name)
        self.sub = self.create_subscription(Image, 'webcam_image', self.listener_callback, 10)
        self.cv_bridge = CvBridge()

    def object_detect(self, image):
        cv2.imshow("object", image)
        cv2.waitKey(10)

    def listener_callback(self, data):
        self.get_logger().info('Receiving video frame')
        image = self.cv_bridge.imgmsg_to_cv2(data, 'bgr8')
        self.object_detect(image)

def main(args=None):
    rclpy.init(args=args)
    node = ImageSubscriber("cam_sub")
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()