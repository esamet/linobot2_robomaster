import sys
sys.path.append('/home/kae/Desktop/RoboMaster-SDK/examples/plaintext_sample_code/RoboMasterEP/connection/network/')
import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from std_msgs.msg import String
import robot_connection

USB_DIRECT_CONNECTION_IP = '192.168.42.2'
robot = robot_connection.RobotConnection(USB_DIRECT_CONNECTION_IP)
if not robot.open():
    print('open fail')
    exit(1)
robot.send_data('command')
recv2 = robot.recv_ctrl_data(5)

class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(Odometry, 'topic', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0
    def sdk_twist(self):
        robot.send_data('chassis speed ?')
        recv = robot.recv_ctrl_data(5)
        x= recv.decode("utf-8")
        x = x.split()
        return x
    def sdk_pose(self):
        robot.send_data('chassis pose ?')
        recv = robot.recv_ctrl_data(5)
        x= recv.decode("utf-8")
        x = x.split()
        return x
    def timer_callback(self):
        msg = Odometry()

        sdk_twist=self.sdk_twist()
        #print(sdk_twist[0])

        
        msg.header.frame_id = "/map"
        msg.child_frame_id = "/base_link"
        msg.pose.pose.position.x=float(sdk_twist[0])
        msg.pose.pose.position.y=float(sdk_twist[1])
        msg.pose.pose.position.z=float(sdk_twist[2])
        msg.pose.pose.orientation.x=float(sdk_twist[0])
        msg.pose.pose.orientation.y=float(sdk_twist[1])
        msg.pose.pose.orientation.z=float(sdk_twist[2])
        msg.pose.pose.orientation.w=float(sdk_twist[2])

        msg.twist.twist.linear.x=float(sdk_twist[0])
        msg.twist.twist.linear.y=float(sdk_twist[1])
        msg.twist.twist.linear.z=float(sdk_twist[2])
        msg.twist.twist.angular.x=4.0
        msg.twist.twist.angular.y=4.0
        msg.twist.twist.angular.z=4.0

        
        self.publisher_.publish(msg)
        self.i += 1


def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher()

    rclpy.spin(minimal_publisher)

    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()