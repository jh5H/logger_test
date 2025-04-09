from rclpy.time import Time
from rclpy.node import Node
import rclpy
from geometry_msgs.msg import Twist
import random


class LoggerTest(Node):
    def __init__(self):
        super().__init__('logger_test')
        
        self.period = 1.0
        self.current_linear = 0.0
        self.current_angular = 0.0
        self.flag = False
        self.speed_limit = 0.5
        self.temp = 0.0

        # subscription of ROS2
        self.cmd_sub_ = self.create_subscription(Twist, '/cmd_vel', self.cmd_callback, 10)
        # timer of ROS2
        self.timer_1 = self.create_timer(self.period, self.timer_callback)
        self.timer_2 = self.create_timer(5, self.speed_camera_callback)
        
    def cmd_callback(self, data):
        self.current_linear = data.linear.x
        self.current_angular = data.angular.z
        
        
    def timer_callback(self):        

        if self.current_linear > self.speed_limit:
            self.get_logger().error(f"현재 속도는 {self.current_linear} 과속 주행중입니다.")

        else:
            self.get_logger().info(f"현재 속도는 {self.current_linear} 정속 주행중입니다.")


    def speed_camera_callback(self):
        
        if self.flag == True :
            self.speed_limit = self.temp
            self.flag = False
            self.get_logger().warn(f"====단속 카메라====")
        else:
            self.temp = random.randint(2, 10)/10
            self.get_logger().warn(f"5초후 {self.temp} m/s 단속 구간입니다.")
            self.flag = True



def main(args=None):

    
    rclpy.init(args=args)
    node = LoggerTest()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()