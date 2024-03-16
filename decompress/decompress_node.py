import rclpy
from rclpy.node import Node
from sensor_msgs.msg import CompressedImage, Image
from cv_bridge import CvBridge
import cv2

class ImageDecompressor(Node):
    def __init__(self):
        super().__init__('image_decompressor')
        self.subscription = self.create_subscription(
            CompressedImage,
            'camera/camera/color/image_raw/compressed',
            self.listener_callback,
            10)
        self.publisher = self.create_publisher(Image, '/camera/color/image_raw', 10)
        self.bridge = CvBridge()

    def listener_callback(self, data):
        try:
            cv_image = self.bridge.compressed_imgmsg_to_cv2(data)
            raw_image_msg = self.bridge.cv2_to_imgmsg(cv_image, "bgr8")
            self.publisher.publish(raw_image_msg)
        except Exception as e:
            self.get_logger().error('Failed to convert image: %r' % (e,))

def main(args=None):
    rclpy.init(args=args)
    image_decompressor = ImageDecompressor()
    rclpy.spin(image_decompressor)
    image_decompressor.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
