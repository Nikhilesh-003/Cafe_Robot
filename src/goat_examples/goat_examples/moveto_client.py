#!/usr/bin/python3


import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from goat_msgs.action import MoveTo

class MoveToClient(Node):
    def __init__(self):
        super().__init__('move_to_client')
        self._action_client = ActionClient(self, MoveTo, 'move_to')

    def send_goal(self, table_numbers):
        goal_msg = MoveTo.Goal()
        goal_msg.table_numbers = table_numbers
        self._action_client.wait_for_server()
        self._action_client.send_goal_async(goal_msg)
        self.get_logger().info(f'Sent goal with tables: {table_numbers}')


def main(args=None):
    rclpy.init(args=args)
    client = MoveToClient()
    table_numbers = input('Enter table numbers (comma separated): ')
    client.send_goal(table_numbers)
    rclpy.spin(client)
    rclpy.shutdown()


if __name__ == '__main__':
    main()

