from numpy import ma
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import csv
import os
import numpy as np
from numpy.lib.npyio import genfromtxt

def receiveData(map_data):
    np.savetxt('subscriber.csv',map_data,delimiter=',',fmt='%s')

class MinimalSubscriber(Node):
    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(String, 'topic', self.listener_callback,5)
        self.subscription

    def listener_callback(self,msg):
        receiveData(eval(msg.data))
        self.get_logger().info('map received')

def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = MinimalSubscriber()
    rclpy.spin(minimal_subscriber)

    minimal_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()