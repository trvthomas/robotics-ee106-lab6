import time
from geometry_msgs.msg import TwistStamped

class MotionControl():
    def move_forward(self, slightlyLeft, slightlyRight):
        self.get_logger().info(f'Moving forward and {'slightly left' if slightlyLeft else ''} {'slightly right' if slightlyRight else ''}')

        vel = TwistStamped()
        vel.twist.linear.x = 2.0
        vel.twist.angular.z = 0.0

        if slightlyLeft:
            vel.twist.angular.z = 6.0
            
        elif slightlyRight:
            vel.twist.angular.z = -4.5
    

        for _ in range(4):
            self.publisher.publish(vel)
            time.sleep(0.1)

    def turn(self, right = False):
        self.get_logger().info(f'Turning {'right' if right else 'left'}')

        vel = TwistStamped()
        vel.twist.linear.x = 0.0
        vel.twist.angular.z = 4.0

        if right:
            vel.twist.angular.z = -3.0

        for _ in range(10):
            self.publisher.publish(vel)
            time.sleep(0.1)