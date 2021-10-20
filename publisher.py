import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import csv
import os
from numpy.lib.npyio import genfromtxt


def importData(input_data):
    global data
    data = input_data

def mapImport():
    file = "map.csv"
    csv_data = genfromtxt("map.csv", delimiter=",")
    importData(csv_data)

class MinimalPublisher(Node):
    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher(String, 'topic', 5)

        timer_period = .5
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        mapImport()
        msg = String()
        msg.data = '%s' % str(data)
        self.publisher.publish(msg)
        self.get_logger().info("Map sent")

def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher()
    rclpy.spin(minimal_publisher)

    minimal_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()