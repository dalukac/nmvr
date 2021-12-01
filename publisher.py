import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import csv
import os
from numpy.lib.npyio import genfromtxt




class MinimalPublisher(Node):
    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher=self.create_publisher(String, 'map', 10)

        timer_period = 1
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i=0

    def timer_callback(self):
        msg=String()
        with open('/home/nmvr/nmvr/nmvr/map.csv', newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',')
            for row in spamreader:
                msg.data+="".join(row)
        self.publisher.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.i += 1

def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher()
    rclpy.spin(minimal_publisher)

    minimal_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()