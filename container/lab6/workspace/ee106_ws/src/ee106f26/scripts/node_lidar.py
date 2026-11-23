#!/usr/bin/env python3

import math, rclpy, numpy, time
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from rclpy.time import Time
from sensor_msgs.msg import LaserScan
from std_msgs.msg import String
from tf2_ros import TransformException
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener

from geometry_msgs.msg import TwistStamped

from tf_transformations import quaternion_matrix
from motion_class import MotionControl


class Lab5Node(Node):
    def __init__(self):
        super().__init__('ranges_check')
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        self.publisher = self.create_publisher(TwistStamped, 'cmd_vel', 5)
        self.subscriber = self.create_subscription(LaserScan, 'scan', self.callback, 5)

        self.turn_count = 0

    def callback(self, scan: LaserScan):
        try:
            t = self.tf_buffer.lookup_transform(
                'left_limit', 'turtlebot4/rplidar_link/rplidar', Time()
            )
        except TransformException:
            self.get_logger().warn('TF not available yet')
            return

        # Get and build transformation matrix T_lidar-left_link
        trans = t.transform.translation
        rot = t.transform.rotation
        T = quaternion_matrix([rot.x, rot.y, rot.z, rot.w])
        T[0:3, 3] = [trans.x, trans.y, trans.z]

        # Loop over all ranges
        left_min_dist = 99
        forward_object = False
        for idx, r in enumerate(scan.ranges):
            if not numpy.isfinite(r):
                continue

            # transform each point
            theta = scan.angle_min + idx * scan.angle_increment
            x_l = r * math.cos(theta)
            y_l = r * math.sin(theta)
            p_lidar = numpy.array([x_l, y_l, 0, 1]) # Point with respect to Lidar
            p_left = T @ p_lidar # Point with respect to left_link

            dist = math.hypot(p_left[0], p_left[1]) # Distance in meters
            #self.get_logger().info(f'Theta = {theta}  and distance = {dist}')
            # Left points
            if (10*math.pi/180) > theta > (-10*math.pi/180) and dist < left_min_dist:
                left_min_dist = dist
            # Forward points
            
            if (-65*math.pi/180) > theta > (-115*math.pi/18) and dist < 0.38:
                forward_object = True


        self.get_logger().info(f'forward? {forward_object} & left dist= {left_min_dist}')

        if self.turn_count > 14:
            self.get_logger().info(f'spining infinitely, find a wall!')
            if(left_min_dist < 1):
                MotionControl.move_forward(self, False, False)
            
            time.sleep(2)

        # Motion control based on conditions
        if 0.1 < left_min_dist < 0.2 and not forward_object:
            MotionControl.move_forward(self, False, False)
            self.turn_count = 0
        elif left_min_dist > 0.5 and not forward_object:
            MotionControl.turn(self)
            self.turn_count += 1
        elif left_min_dist > 0.5 and forward_object:
            MotionControl.turn(self, True)
            self.turn_count += 1
        elif left_min_dist > 0.2 and not forward_object:
            MotionControl.move_forward(self, True, False)
            self.turn_count = 0
        elif left_min_dist < 0.1 and not forward_object:
            MotionControl.move_forward(self, False, True)
            self.turn_count = 0
        else:
            MotionControl.turn(self, True)
            self.turn_count += 1

def main(args=None):
    rclpy.init(args=args)

    node = Lab5Node()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()