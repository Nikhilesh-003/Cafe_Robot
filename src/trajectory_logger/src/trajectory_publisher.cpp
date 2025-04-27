#include "rclcpp/rclcpp.hpp"
#include "geometry_msgs/msg/pose_stamped.hpp"
#include "nav_msgs/msg/path.hpp"
#include "nav_msgs/msg/odometry.hpp"
#include "visualization_msgs/msg/marker_array.hpp"
#include "trajectory_logger/srv/SaveTrajectory.hpp"

#include <vector>
#include <fstream>

class TrajectoryPublisher : public rclcpp::Node {
public:
    TrajectoryPublisher() : Node("trajectory_publisher") {
        path_publisher_ = this->create_publisher<nav_msgs::msg::Path>("trajectory_path", 10);
        marker_publisher_ = this->create_publisher<visualization_msgs::msg::MarkerArray>("trajectory_markers", 10);

        odom_subscriber_ = this->create_subscription<nav_msgs::msg::Odometry>(
            "/odom", 10, std::bind(&TrajectoryPublisher::odomCallback, this, std::placeholders::_1));

        save_service_ = this->create_service<trajectory_logger::srv::SaveTrajectory>(
            "save_trajectory", 
            std::bind(&TrajectoryPublisher::saveTrajectory, this, std::placeholders::_1, std::placeholders::_2));

        timer_ = this->create_wall_timer(std::chrono::milliseconds(100), 
            std::bind(&TrajectoryPublisher::publishTrajectory, this));

        RCLCPP_INFO(this->get_logger(), "Trajectory Publisher Node Started!");
    }

private:
    rclcpp::Publisher<nav_msgs::msg::Path>::SharedPtr path_publisher_;
    rclcpp::Publisher<visualization_msgs::msg::MarkerArray>::SharedPtr marker_publisher_;
    rclcpp::Subscription<nav_msgs::msg::Odometry>::SharedPtr odom_subscriber_;
    rclcpp::Service<trajectory_logger::srv::SaveTrajectory>::SharedPtr save_service_;
    rclcpp::TimerBase::SharedPtr timer_;

    nav_msgs::msg::Path path_msg_;
    std::vector<geometry_msgs::msg::PoseStamped> trajectory_;

    void odomCallback(const nav_msgs::msg::Odometry::SharedPtr msg) {
        geometry_msgs::msg::PoseStamped pose;
        pose.header = msg->header;
        pose.pose = msg->pose.pose;

        trajectory_.push_back(pose);
        RCLCPP_INFO(this->get_logger(), "Added point: x=%.2f, y=%.2f, z=%.2f",
                    pose.pose.position.x, pose.pose.position.y, pose.pose.position.z);
    }

    void publishTrajectory() {
        if (trajectory_.empty()) return;

        path_msg_.header.stamp = this->get_clock()->now();
        path_msg_.header.frame_id = "map";
        path_msg_.poses = trajectory_;
        path_publisher_->publish(path_msg_);

        publishMarkers();
    }

    void publishMarkers() {
        visualization_msgs::msg::MarkerArray marker_array;
        visualization_msgs::msg::Marker marker;

        marker.header.frame_id = "map";
        marker.ns = "trajectory";
        marker.type = visualization_msgs::msg::Marker::SPHERE_LIST;
        marker.action = visualization_msgs::msg::Marker::ADD;
        marker.scale.x = 0.1;
        marker.scale.y = 0.1;
        marker.scale.z = 0.1;
        marker.color.a = 1.0;
        marker.color.r = 1.0;
        
        for (const auto& pose : trajectory_) {
            marker.points.push_back(pose.pose.position);
        }

        marker_array.markers.push_back(marker);
        marker_publisher_->publish(marker_array);
    }

    void saveTrajectory(const std::shared_ptr<trajectory_logger::srv::SaveTrajectory::Request> request,
                        std::shared_ptr<trajectory_logger::srv::SaveTrajectory::Response> response) {
        std::ofstream file(request->filename);
        if (!file) {
            response->success = false;
            response->message = "Failed to open file";
            RCLCPP_ERROR(this->get_logger(), "Failed to open file: %s", request->filename.c_str());
            return;
        }

        for (const auto& pose : trajectory_) {
            file << pose.pose.position.x << "," 
                 << pose.pose.position.y << "," 
                 << pose.pose.position.z << "\n";
        }

        response->success = true;
        response->message = "Trajectory saved successfully";
        RCLCPP_INFO(this->get_logger(), "Trajectory saved to %s", request->filename.c_str());
    }
};

int main(int argc, char **argv) {
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<TrajectoryPublisher>());
    rclcpp::shutdown();
    return 0;
}

