import rclpy
from rclpy.node import Node
from interfaces.srv import MoveServo


class Servo_Client(Node):
    def __init__(self):
        super().__init__('servo_Client')
    
        self.cli = self.create_client(MoveServo, 'turn_servo')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = MoveServo.Request()
        
    def send_request(self, port, pos):
        self.req.port = port
        self.req.pos = pos
        self.future = self.cli.call_async(self.req)
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()
    
    def USB_request(self):
        #Move servo on port 0 to minimum position
        servo1 = MoveServo.Request()
        servo1.port = 0
        servo1.pos = 2432
        
        response = Servo_Client.send_request(servo1.port, servo1.pos)
        Servo_Client.get_logger().info(
            'Results: %s, status: %s' %
            (response.status, response.status_msg))
        
        
        #Move servo on port 5 to maximum position
        servo2 = MoveServo.Request()
        servo2.port = 5
        servo2.pos = 9600
        
        response = Servo_Client.send_request(servo2.port, servo2.pos)
        Servo_Client.get_logger().info(
            'Results: %s, status: %s' %
            (response.status, response.status_msg))
        
    def i2c_request(self):
        #Move servo on port 0 to minimum position
        servo1 = MoveServo.Request()
        servo1.port = 0
        servo1.pos = 0
        
        response = Servo_Client.send_request(servo1.port, servo1.pos)
        Servo_Client.get_logger().info(
            'Results: %s, status: %s' %
            (response.status, response.status_msg))
        
        
        #Move servo on port 5 to maximum position
        servo2 = MoveServo.Request()
        servo2.port = 5
        servo2.pos = 180
        
        response = Servo_Client.send_request(servo2.port, servo2.pos)
        Servo_Client.get_logger().info(
            'Results: %s, status: %s' %
            (response.status, response.status_msg))
            
    
    
def main(args=None):
    rclpy.init(args=args)
    servo_Client = Servo_Client()
    
    Servo_Client.USB_request()
    
    Servo_Client.i2c_request()
    

    servo_Client.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()