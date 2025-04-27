#!/usr/bin/env python3


import rclpy
import time
from rclpy.node import Node
from rclpy.action import ActionServer, GoalResponse, CancelResponse
from rclpy.action import ActionClient
from action_msgs.msg import GoalStatus
from goat_msgs.action import FoodDelivery 
from nav2_msgs.action import NavigateToPose
from geometry_msgs.msg import PoseStamped, Quaternion
import tf_transformations


class FoodDeliveryServer(Node):
   def __init__(self):
       super().__init__('food_delivery_server')


       self.home_pose = (-4.625, 4.245)
       self.kitchen_pose = (1.5, 3.0)
       self.table_poses = {
           1: (2.05, -3.28),
           2: (1.84, -7.50),
           3: (-3.26, -7.75)
       }


       self._action_server = ActionServer(
           self,
           FoodDelivery,
           'food_delivery',
           execute_callback=self.execute_callback,
           goal_callback=self.goal_callback,
           cancel_callback=self.cancel_callback
       )


       self.nav_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')


       self.current_goal_handle = None
       self.cancel_requested = False


   def goal_callback(self, goal_request):
       self.get_logger().info("Received a new delivery request.")
       return GoalResponse.ACCEPT


   def cancel_callback(self, goal_handle):
       self.get_logger().info("Cancel request received!")
       self.cancel_requested = True
       return CancelResponse.ACCEPT


   async def execute_callback(self, goal_handle):
       self.current_goal_handle = goal_handle
       tables = goal_handle.request.tables  
       require_confirmation = goal_handle.request.require_confirmation


       if await self.navigate_to(self.kitchen_pose, "Kitchen"):
           return self.abort(goal_handle, "Failed to reach kitchen!")


       if require_confirmation:
           self.get_logger().info("Waiting for confirmation at the Kitchen...")
           if not await self.wait_for_confirmation("Kitchen"):
               self.get_logger().info("No confirmation at the Kitchen. Returning to Home.")
               await self.navigate_to(self.home_pose, "Home")
               goal_handle.succeed()
               return FoodDelivery.Result(success=False)


       for table in tables:
           if self.cancel_requested:
               self.get_logger().info("Task canceled. Returning to Home.")
               await self.navigate_to(self.home_pose, "Home")
               goal_handle.succeed()
               return FoodDelivery.Result(success=False)


           if table not in self.table_poses:
               self.get_logger().warn(f"Table {table} not found!")
               continue


           if await self.navigate_to(self.table_poses[table], f"Table {table}"):
               return self.abort(goal_handle, f"Failed to reach Table {table}!")


           if require_confirmation:
               self.get_logger().info(f"Waiting for confirmation at Table {table}...")
               if not await self.wait_for_confirmation(f"Table {table}"):
                   self.get_logger().info(f"No confirmation at Table {table}. Returning to Kitchen.")
                   await self.navigate_to(self.kitchen_pose, "Kitchen")
                   await self.navigate_to(self.home_pose, "Home")
                   goal_handle.succeed()
                   return FoodDelivery.Result(success=False)


       await self.navigate_to(self.kitchen_pose, "Kitchen")
       await self.navigate_to(self.home_pose, "Home")


       self.get_logger().info("Delivery Completed Successfully.")
       goal_handle.succeed()
       return FoodDelivery.Result(success=True)




   async def navigate_to(self, target_pose, location_name):
       """ Sends a navigation goal to the Nav2 action server. """
       self.get_logger().info(f"Navigating to {location_name} at {target_pose}...")
       goal_msg = NavigateToPose.Goal()
       goal_msg.pose.header.frame_id = "map"
       goal_msg.pose.header.stamp = self.get_clock().now().to_msg()
       goal_msg.pose.pose.position.x = target_pose[0]
       goal_msg.pose.pose.position.y = target_pose[1]
       quaternion = tf_transformations.quaternion_from_euler(0, 0, 0)
       goal_msg.pose.pose.orientation = Quaternion(
           x=quaternion[0], y=quaternion[1], z=quaternion[2], w=quaternion[3]
       )
       if not self.nav_client.wait_for_server(timeout_sec=5.0):
           self.get_logger().error("Nav2 action server not available!")
           return True
       self.get_logger().info(f"Sending navigation goal to {location_name}...")
       future = self.nav_client.send_goal_async(goal_msg)


       goal_handle = await future
       if not goal_handle.accepted:
           self.get_logger().error(f"Goal to {location_name} was rejected!")
           return True
       result_future = goal_handle.get_result_async()
       result = await result_future


       if result.status == GoalStatus.STATUS_SUCCEEDED:
           self.get_logger().info(f"Successfully reached {location_name}.")
           return False 
       else:
           self.get_logger().error(f"Failed to reach {location_name}.")
           return True 


   async def wait_for_confirmation(self, location_name):
       """ Waits for confirmation at a given location. """
       self.get_logger().info(f"Waiting for confirmation at {location_name}...")
       timeout = 10  
       start_time = time.time()


       while time.time() - start_time < timeout:
           if self.cancel_requested:
               return False


           confirmation = input(f"Enter 'confirm' to proceed from {location_name}: ")
           if confirmation.lower() == "confirm":
               self.get_logger().info(f"Confirmation received at {location_name}.")
               return True
           time.sleep(1)


       self.get_logger().info(f"Confirmation timeout at {location_name}!")
       return False










def main(args=None):
   rclpy.init(args=args)
   node = FoodDeliveryServer()
   rclpy.spin(node)
   node.destroy_node()
   rclpy.shutdown()


if __name__ == '__main__':
   main()