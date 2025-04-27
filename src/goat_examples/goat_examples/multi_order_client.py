#!/usr/bin/env python3

import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from goat_msgs.action import MultiOrder

class MultiOrderClient(Node):

    def __init__(self):
        super().__init__('MultiOrder_client')
        self._action_client = ActionClient(self, MultiOrder, 'multi_order')

    def send_goal(self, tables):
        goal_msg = MultiOrder.Goal()
        goal_msg.tables = tables

        self._action_client.wait_for_server()
        self._send_goal_future = self._action_client.send_goal_async(goal_msg)
        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected.')
            return

        self.get_logger().info('Goal accepted.')

        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        result = future.result().result
        if result.success:
            self.get_logger().info('Navigation succeeded.')
        else:
            self.get_logger().info('Navigation failed.')

def main(args=None):
    rclpy.init(args=args)
    client = MultiOrderClient()

    table_numbers = input("Enter table numbers (comma separated): ")
    client.send_goal(table_numbers)
    rclpy.spin(client)

if __name__ == '__main__':
    main()
