#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import qrcode
import cv2
import numpy as np

class QRCodeNode(Node):
    def __init__(self):
        super().__init__('rostime_qr_node')
        
        # Timer to generate and publish the QR code at regular intervals
        self.IMG_MAX_VALUE = 255
        self.timer_period = 0.1  # 1 second update rate
        self.timer = self.create_timer(self.timer_period, self.timer_callback)
        
        self.window_name = "ROS 2 Time QR Code"
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
        
        # Create an instance of CvBridge to convert OpenCV images to ROS Image messages
        self.bridge = CvBridge()

        self.get_logger().info("[ROSTimeQRCode] Initialized ROS 2 time to QR code node. Press CTRL + C to shutdown.")


    def generate_qr_code(self, data):
        """Generate a QR code image from the given data."""
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=20,
            border=5,
        )
        qr.add_data(data)
        qr.make(fit=True)
 
        # Convert QR code to an OpenCV-compatible format
        img = np.array(qr.make_image(), dtype=np.uint8)
        return self.IMG_MAX_VALUE * img

    def timer_callback(self):
        # Get the current ROS time as a string
        current_time = self.get_clock().now()
        time_str = f"{current_time.nanoseconds / 1e9:.9f}"

        # self.get_logger().info(time_str)
 
        # Generate QR code for the current time
        qr_image = self.generate_qr_code(time_str)

        cv2.putText(qr_image, f'ROS Time: {time_str}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, thickness=1, color=(0, 0, 0))

        # Display the QR code using OpenCV
        cv2.imshow(self.window_name, qr_image)
        if cv2.waitKey(1) == 27:
            cv2.destroyAllWindows()

def main(args=None):
    rclpy.init(args=args)
    qr_code_node = QRCodeNode()
    try:
        rclpy.spin(qr_code_node)
    except KeyboardInterrupt:
        qr_code_node.destroy_node()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()