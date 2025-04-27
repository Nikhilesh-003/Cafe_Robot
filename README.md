**Cafe Butler Robot**

Software Used:
> OS: Ubuntu 22.04

> Framework: ROS2 Humble

> Simulation Engine: Gazebo Fortress

> Robot: BCR_Bot (Delivery Robot from Black Coffee Robotics)


A custom world was created using the elements from OpenRobotics present in GazeboSim App. 

**Objective:**

The orders are received by the robot, which makes it to travel to the kitchen to collect food, 
and moves to the customers' tables to deliver. Once the order is completed, the robot will move to its initial
home position.


**Description of the Project:**

●​ The nav2_simple_commander package is used for autonomous navigation.

●​ Tkinter, a python library is used to create a simple GUI for the user to select a table for food
delivery in the cafe. 

●​ Usage of ROS2 Action Server and Client to set the goal pose and obtain the robot's feedback towards goal continuously. 


To launch the robot:
```bash
ros2 launch goat_description ign.launch.py
```

![Screenshot from 2025-04-27 11-14-07](https://github.com/user-attachments/assets/37c3730e-8d77-42a8-9c8d-eee87452b205)

