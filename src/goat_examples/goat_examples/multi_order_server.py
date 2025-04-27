#!/usr/bin/env python3

import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node
from nav2_simple_commander.robot_navigator import BasicNavigator
from geometry_msgs.msg import PoseStamped
from goat_msgs.action import MultiOrder

class MultiOrderServer(Node):

    def __init__(self):
        super().__init__('multi_order_server')
        self.navigator = BasicNavigator()

        # Define pre-set table positions
        self.table_poses = {
            1: (2.05, -3.28),
            2: (1.84, -7.50),
            3: (-3.26, -7.75),
            4: (4.0, -2.0)
        }

        # Create an action server
        self._action_server = ActionServer(
            self,
            MultiOrder,
            'multi_order',
            self.execute_callback
        )

    def execute_callback(self, goal_handle):
        self.get_logger().info('Executing multi-order navigation...')

        # Parse user inputs
        tables = list(map(int, goal_handle.request.tables.split(',')))
        canceled_tables = list(map(int, goal_handle.request.canceled_tables.split(',')))

        for table in tables:
            if table in canceled_tables:
                self.get_logger().info(f'Navigation to table {table} canceled.')
                continue

            if table not in self.table_poses:
                self.get_logger().warn(f'Table {table} does not exist.')
                continue

            pose = self.create_goal_pose(self.table_poses[table])
            self.navigator.goToPose(pose)

            while not self.navigator.isTaskComplete():
                feedback_msg = MultiOrder.Feedback()
                feedback_msg.feedback = f'Navigating to table {table}...'
                self.get_logger().info(feedback_msg.feedback)
                goal_handle.publish_feedback(feedback_msg)

            result = self.navigator.getResult()
            if result == "SUCCEEDED":
                self.get_logger().info(f'Successfully reached table {table}.')
            else:
                self.get_logger().error(f'Failed to reach table {table}. Aborting...')
                goal_handle.abort()
                return MultiOrder.Result(success=False)

        goal_handle.succeed()
        return MultiOrder.Result(success=True)

    def create_goal_pose(self, position):
        pose = PoseStamped()
        pose.header.frame_id = "map"
        pose.pose.position.x, pose.pose.position.y = position
        pose.pose.orientation.w = 1.0
        return pose

def main(args=None):
    rclpy.init(args=args)
    node = MultiOrderServer()
    rclpy.spin(node)

if __name__ == '__main__':
    main()
