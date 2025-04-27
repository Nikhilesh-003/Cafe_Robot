#!/usr/bin/env python3


import rclpy
from rclpy.node import Node
from goat_msgs.action import FoodDelivery 
from rclpy.action import ActionClient


class FoodDeliveryClient(Node):
   def __init__(self):
       super().__init__('food_delivery_client')
       self._action_client = ActionClient(self, FoodDelivery, 'food_delivery')


   def send_goal(self, table, require_confirmation):
       goal_msg = FoodDelivery.Goal()
       goal_msg.tables = [table]
       goal_msg.require_confirmation = require_confirmation


       confirmation_text = input("Enter 'confirm' to proceed to the table: ")
       goal_msg.confirmation_text = confirmation_text


       self._action_client.wait_for_server()
       self._send_goal_future = self._action_client.send_goal_async(goal_msg)
       self._send_goal_future.add_done_callback(self.goal_response_callback)


   def goal_response_callback(self, future):
       goal_handle = future.result()
       if not goal_handle.accepted:
           self.get_logger().info('Goal rejected')
           return


       self.get_logger().info('Goal accepted')
       self._get_result_future = goal_handle.get_result_async()
       self._get_result_future.add_done_callback(self.get_result_callback)


   def get_result_callback(self, future):
       result = future.result().result
       if result.success:
           self.get_logger().info("Delivery completed successfully!")
       else:
           self.get_logger().info("Delivery failed or timed out.")
       rclpy.shutdown()


def main(args=None):
   rclpy.init(args=args)
   client = FoodDeliveryClient()
   table_number = int(input("Enter the table number (1/2/3): "))
   require_confirmation = bool(int(input("Require confirmation? (1 for Yes / 0 for No): ")))
   client.send_goal(table_number, require_confirmation)
   rclpy.spin(client)


if __name__ == '__main__':
   main()