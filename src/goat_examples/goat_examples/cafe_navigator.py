#!/usr/bin/env python3

from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
import rclpy
import tkinter as tk
from ament_index_python.packages import get_package_share_directory
import os
import subprocess

class NavigatorApp:
    def __init__(self):
        self.navigator = BasicNavigator()
        self.home_pose = (-4.625, 4.245)
        self.kitchen_pose = (1.5, 3.0)
        self.table_poses = {
            1: (2.05, -3.28),
            2: (1.84, -7.50),
            3: (-3.26, -7.75)
        }
        self.tk_button = tk.Tk()
        self.tk_button.title("Food Delivery Robot")
        for table_number, pose in self.table_poses.items():
            self.create_button(f'Table {table_number}', table_number)
        self.set_initial_pose()

    def create_button(self, text, table_number):
        button = tk.Button(self.tk_button, text=text, command=lambda: self.handle_order(table_number))
        button.pack()

    def set_initial_pose(self):
        initial_pose = PoseStamped()
        initial_pose.header.frame_id = 'map'
        initial_pose.header.stamp = self.navigator.get_clock().now().to_msg()
        initial_pose.pose.position.x = self.home_pose[0]
        initial_pose.pose.position.y = self.home_pose[1]
        initial_pose.pose.orientation.w = 0.99
        self.navigator.setInitialPose(initial_pose)
        self.navigator.waitUntilNav2Active()
        print("[INFO] Initial pose set to Home.")

    def move_to_pose(self, x, y):
        goal_pose = PoseStamped()
        goal_pose.header.frame_id = 'map'
        goal_pose.header.stamp = self.navigator.get_clock().now().to_msg()
        goal_pose.pose.position.x = x
        goal_pose.pose.position.y = y
        goal_pose.pose.orientation.w = 0.99
        self.navigator.goToPose(goal_pose)
        while not self.navigator.isTaskComplete():
            feedback = self.navigator.getFeedback()
            if feedback:
                print(f"[INFO] Moving to x: {x}, y: {y} ")
        result = self.navigator.getResult()
        if result == TaskResult.SUCCEEDED:
            print("[INFO] Goal succeeded!")
        else:
            print("[ERROR] Goal failed!")

    def handle_order(self, table_number):
        print(f"[INFO] Order received for Table {table_number}")

        print("[INFO] Moving to Kitchen")
        self.move_to_pose(self.kitchen_pose[0], self.kitchen_pose[1])

        table_pose = self.table_poses[table_number]
        print(f"[INFO] Moving to Table {table_number}")
        self.move_to_pose(table_pose[0], table_pose[1])

        print("[INFO] Returning to Home")
        self.move_to_pose(self.home_pose[0], self.home_pose[1])

        print(f"[INFO] Delivery to Table {table_number} completed.")

    def exiting(self):
        self.tk_button.mainloop()
        self.navigator.lifecycleShutdown()

def start_app():
    rclpy.init()
    app = NavigatorApp()
    app.exiting()
    rclpy.shutdown()

if __name__ == '__main__':
    start_app()
