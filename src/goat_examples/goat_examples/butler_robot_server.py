#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer
from goat_msgs.action import ButlerRobot
from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult

class ButlerRobotServer(Node):

    def __init__(self):
        super().__init__('butler_robot_server')
        self._action_server = ActionServer(
            self,
            ButlerRobot,
            'butler_robot',
            self.execute_callback)
        self.navigator = BasicNavigator()
        self.get_logger().info("Butler Robot Action Server Started")

        # Table coordinates dictionary
        self.table_coordinates = {
            1: (2.05, -3.28),
            2: (1.84, -7.50),
            3: (-3.26, -7.75)
        }

    def set_pose(self, x, y, w=0.99):
        pose = PoseStamped()
        pose.header.frame_id = 'map'
        pose.header.stamp = self.navigator.get_clock().now().to_msg()
        pose.pose.position.x = x
        pose.pose.position.y = y
        pose.pose.orientation.w = w
        return pose

    def execute_callback(self, goal_handle):
        self.get_logger().info(f'Received Order: Table {goal_handle.request.table_number}, Order ID: {goal_handle.request.order_id}')

        # Feedback
        feedback_msg = ButlerRobot.Feedback()

        # Initial Pose (Spawn Location)
        initial_pose = self.set_pose(-4.625, 4.245)
        self.navigator.setInitialPose(initial_pose)
        self.navigator.waitUntilNav2Active()

        # Moving to the Counter/Kitchen
        feedback_msg.status_message = 'Moving to Counter/Kitchen'
        goal_handle.publish_feedback(feedback_msg)
        kitchen_pose = self.set_pose(1.5, 3.0)
        self.navigator.goToPose(kitchen_pose)

        while not self.navigator.isTaskComplete():
            feedback_msg.status_message = 'Reaching Counter/Kitchen...'
            goal_handle.publish_feedback(feedback_msg)

        # Check success for kitchen
        if self.navigator.getResult() != TaskResult.SUCCEEDED:
            goal_handle.abort()
            return ButlerRobot.Result(success=False, result_message='Failed to reach Counter/Kitchen')

        feedback_msg.status_message = 'Reached Counter/Kitchen'
        goal_handle.publish_feedback(feedback_msg)

        # Get the coordinates of the target table
        table_number = goal_handle.request.table_number
        if table_number not in self.table_coordinates:
            goal_handle.abort()
            return ButlerRobot.Result(success=False, result_message=f'Table {table_number} not found')

        x, y = self.table_coordinates[table_number]

        # Moving to the specified table
        feedback_msg.status_message = f'Moving to Table {table_number}'
        goal_handle.publish_feedback(feedback_msg)
        table_pose = self.set_pose(x, y)
        self.navigator.goToPose(table_pose)

        while not self.navigator.isTaskComplete():
            feedback_msg.status_message = f'Approaching Table {table_number}...'
            goal_handle.publish_feedback(feedback_msg)

        # Check success for the table
        if self.navigator.getResult() == TaskResult.SUCCEEDED:
            goal_handle.succeed()
            return ButlerRobot.Result(success=True, result_message=f'Successfully delivered to Table {table_number}')
        else:
            goal_handle.abort()
            return ButlerRobot.Result(success=False, result_message=f'Failed to reach Table {table_number}')

def main(args=None):
    rclpy.init(args=args)
    server = ButlerRobotServer()
    rclpy.spin(server)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
