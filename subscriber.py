from numpy import ma
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import csv
import os
import numpy as np
from numpy.lib.npyio import genfromtxt


class MinimalSubscriber(Node):
    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(String, 'map', self.listener_callback,100)
        self.subscription

    def listener_callback(self,msg):
        self.get_logger().info('I heard: "%s"' % msg.data)
        grid=msg.data
        with open('/home/nmvr/nmvr/nmvr/map.csv', 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for pos in grid:
                spamwriter.writerow(str(pos))

def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = MinimalSubscriber()
    rclpy.spin(minimal_subscriber)

    minimal_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()