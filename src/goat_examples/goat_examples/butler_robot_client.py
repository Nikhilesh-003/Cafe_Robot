#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from goat_msgs.action import ButlerRobot

class ButlerRobotClient(Node):

    def __init__(self):
        super().__init__('butler_robot_client')
        self._action_client = ActionClient(self, ButlerRobot, 'butler_robot')

    def send_order(self, table_number, order_id):
        goal_msg = ButlerRobot.Goal()
        goal_msg.table_number = table_number
        goal_msg.order_id = order_id

        self._action_client.wait_for_server()
        self._send_goal_future = self._action_client.send_goal_async(
            goal_msg, feedback_callback=self.feedback_callback)
        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Order Rejected')
            return
        self.get_logger().info('Order Accepted')
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def feedback_callback(self, feedback_msg):
        self.get_logger().info(f'Feedback: {feedback_msg.feedback.status_message}')

    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info(f'Result: {result.result_message}')

def main(args=None):
    rclpy.init(args=args)
    client = ButlerRobotClient()
    table_number = int(input("Enter Table Number: "))
    order_id = input("Enter Order ID: ")
    client.send_order(table_number, order_id)
    rclpy.spin(client)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
