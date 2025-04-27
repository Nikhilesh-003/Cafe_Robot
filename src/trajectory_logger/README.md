# 🚀ROS2 Trajectory Logger & Visualizer📍
This ROS2 package enables real-time trajectory collection, storage, and visualization for mobile robots. It consists of two key nodes:

✅ Trajectory Publisher and Saver Node
- 📝 Collects and publishes the robot's trajectory as a marker array.
- 💾 Provides a ROS service to save trajectory data in JSON, CSV, or YAML formats.
- ⏳ Allows users to specify a time duration for saving recent trajectory data.

✅ Trajectory Reader and Publisher Node
- 📂 Reads saved trajectory files.
- 🔄 Transforms the trajectory to the odom frame.
- 📡 Publishes the transformed trajectory for visualization.

This package is ideal for path tracking, debugging, and performance analysis in robotics applications using ROS2. 🤖✨

---

## 🚀 Features  

✅ **Real-Time Trajectory Collection – Captures the robot’s movement dynamically.**  
✅ **Flexible Data Storage – Save trajectories in JSON, CSV, or YAML formats.**  
✅ **Time-Based Logging – Save only the last N seconds of trajectory data.**  
✅ **Visualization with Markers – Publishes trajectories as ROS2 Marker Arrays for visualization in RViz.**  
✅ **Frame Transformation – Reads and transforms trajectories into the odom frame for accurate positioning.**  
✅ **Custom ROS2 Service – Save trajectory data on demand with a simple service call.**  

---

## 🛠️ Installation  

### 1️⃣ **Clone the Repository**  
```bash
cd ~/ros_ws/src
git clone https://github.com/yashbhaskar/ROS2_Trajectory_Logger_And_Visualizer.git
cd ~/ros_ws
```

### 2️⃣ **Build the Package** 
```bash
colcon build --packages-select trajectory_logger
source install/setup.bash
```

---

## 🎮 Usage

### 1️⃣ Launch Robot Autobringup launch file (Tortoisebot) Of any Robot:
```bash
ros2 launch tortoisebot_bringup autobringup.launch.py use_sim_time:=True exploration:=True
```
After Spawn robot. Give 2d goal to robot in rviz2.

### 2️⃣ Start trajectory collection Node:
```bash
ros2 run trajectory_logger trajectory_publisher
```
Collects and publishes the robot's trajectory in real time.

### 3️⃣ Save trajectory data using Service:
```bash
ros2 service call /save_trajectory trajectory_logger/srv/SaveTrajectory "{filename: \"trajectory.json\", duration: 10}"
```
Saves the last 10 seconds of trajectory data to a file.

### 4️⃣ Read & Visualize Trajectory:
```bash
ros2 run trajectory_logger trajectory_reader
```
Reads and publishes saved trajectory data for visualization in RViz.
In RViz, click "Add" → Select "MarkerArray" → Set the topic to /read_trajectory.
Now, you should see the robot's path displayed!

---
## 🎯 Final Result: Visualized Robot Trajectory in RViz:
![Screenshot from 2025-03-04 23-53-37](https://github.com/user-attachments/assets/4aaec3f8-6a6a-4664-8d0d-167fddbd4025)
This image showcases the robot's trajectory visualization in a mapped environment using ROS2 and RViz.

---

## 📽️ Video Demonstration: Robot Trajectory Tracking & Visualization in ROS2

https://drive.google.com/file/d/1xaM5Kn9YMzeJ0jUUFf2rSthsn5pK-VOP/view

---

## 📡 Flowchart:
This flowchart illustrates the process of collecting, saving, and visualizing a robot's trajectory using ROS2.
![Untitled Diagram drawio](https://github.com/user-attachments/assets/48f683cf-ea5b-4a72-8182-b92143e600ff)

---

## ⚙️ Algorithm for Trajectory Processing

1. Start the trajectory processing system
2. Initialize necessary ROS2 nodes
    - Create the Publisher Node for publishing trajectory markers.
    - Create the Saver Node for storing trajectory data.
    - Create the Reader Node for loading and publishing stored trajectories.
3. Subscribe to the robot's pose topic
    - Retrieve pose information (x, y, z, orientation).
    - Store pose data in a trajectory list.
4. Continuously collect robot’s pose data
    - Append each pose update to the trajectory list.
5. Publish the trajectory as a MarkerArray
    - Convert trajectory points into ROS visualization markers.
    - Publish them to be visualized in RViz.
6. Check if the user requests to save trajectory data
    - If YES, proceed to Step 7.
    - If NO, continue collecting trajectory data.
7. Save trajectory data to a file
    - Allow the user to specify:
        - Filename (e.g., trajectory.json, trajectory.csv)
        - Duration (e.g., last 10 seconds of data)
    - Extract the trajectory data for the specified duration.
    - Format and store data in JSON, CSV, or YAML format.
    - Confirm that the file has been saved successfully.
8. Check if the user requests to load a saved trajectory
    - If YES, proceed to Step 9.
    - If NO, end the process.
9. Read the stored trajectory data from the file
    - Parse the selected file format (JSON, CSV, or YAML).
10. Transform trajectory data to the odom frame
    - Ensure consistency between the stored data and the current robot environment.
11. Publish the loaded trajectory for visualization
    - Convert the loaded trajectory to MarkerArray format.
    - Publish the trajectory to RViz for display.
12. Continue collecting new trajectory data or exit
    - If the user stops the process, terminate trajectory collection.
    - Shut down ROS nodes gracefully.

---

## 📂 Project Structure:
```
trajectory_logger/
│── include/
│   ├── trajectory_logger/
│── src/
│   ├── trajectory_publisher.cpp    # Trajectory Publisher and Saver Node
│   ├── trajectory_reader.cpp       # Trajectory Reader and Publisher Node
│── srv/
│   ├── SaveTrajectory.srv
│── CMakeLists.txt                  # CMake build configuration
│── package.xml
│── README.md
```

---

## 🤝 Contributing

Feel free to fork this repository, create a pull request, or open an issue if you have suggestions or find bugs.

---

## ✉️ Contact

📧 Yash Bhaskar – ybbhaskar19@gmail.com
📌 GitHub: https://github.com/yashbhaskar




