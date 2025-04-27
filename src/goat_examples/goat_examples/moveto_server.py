#!/usr/bin/python3
import rclpy
from rclpy.node import Node
from nav2_msgs.action import NavigateToPose
from goat_msgs.action import MoveTo
from rclpy.action import ActionServer, ActionClient
from geometry_msgs.msg import PoseStamped
from rclpy.executors import MultiThreadedExecutor

class MoveToServer(Node):
    def __init__(self):
        super().__init__('move_to_server')
        self._action_server = ActionServer(
            self,
            MoveTo,
            'move_to',
            self.execute_callback)
        self.nav_action_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')
        self.get_logger().info('MoveTo action server started.')

    def move_to(self, position):
        if not self.nav_action_client.wait_for_server(timeout_sec=5.0):
            self.get_logger().error('Navigation action server not available.')
            return False

        goal_msg = NavigateToPose.Goal()
        goal_msg.pose.header.frame_id = 'map'
        goal_msg.pose.pose.position.x = position[0]
        goal_msg.pose.pose.position.y = position[1]
        goal_msg.pose.pose.orientation.w = 1.0

        self.get_logger().info(f'Moving to position ({position[0]}, {position[1]})...')

        future = self.nav_action_client.send_goal_async(goal_msg)
        rclpy.spin_until_future_complete(self, future)

        if future.result() and future.result().status == 3:
            self.get_logger().info('Arrived at destination.')
            return True
        else:
            self.get_logger().error(f'Failed to move to ({position[0]}, {position[1]})')
            return False

    def execute_callback(self, goal_handle):
        self.get_logger().info('Executing goal...')

        locations = {
            'home': (-4.625, 4.245),
            'kitchen': (1.5, 3.0),
            'table1': (2.05, -3.28),
            'table2': (-1.5, -4.0),
            'table3': (-3.26, -7.75)
        }

        for table in goal_handle.request.target_locations:
            location = locations.get(table, None)
            if location:
                if not self.move_to(location):
                    self.get_logger().info(f'Failed to move to {table}.')
                    goal_handle.abort()
                    return MoveTo.Result()

        self.get_logger().info('Task completed successfully!')
        goal_handle.succeed()
        return MoveTo.Result()


def main(args=None):
    rclpy.init(args=args)
    move_to_server = MoveToServer()
    executor = MultiThreadedExecutor()
    rclpy.spin(move_to_server, executor=executor)
    move_to_server.destroy()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
