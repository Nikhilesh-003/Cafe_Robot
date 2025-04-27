#include "rclcpp/rclcpp.hpp"
#include "visualization_msgs/msg/marker_array.hpp"
#include "geometry_msgs/msg/point.hpp"
#include <fstream>
#include <sstream>
#include <vector>

class TrajectoryReader : public rclcpp::Node {
public:
    TrajectoryReader() : Node("trajectory_reader") {
        marker_publisher_ = this->create_publisher<visualization_msgs::msg::MarkerArray>("read_trajectory", 10);
        timer_ = this->create_wall_timer(std::chrono::seconds(1), std::bind(&TrajectoryReader::publishMarkers, this));

        loadTrajectory("trajectory.json"); 
    }

private:
    rclcpp::Publisher<visualization_msgs::msg::MarkerArray>::SharedPtr marker_publisher_;
    rclcpp::TimerBase::SharedPtr timer_;
    std::vector<geometry_msgs::msg::Point> trajectory_;

    void loadTrajectory(const std::string &filename) {
        std::ifstream file(filename);
        if (!file.is_open()) {
            RCLCPP_ERROR(this->get_logger(), "Failed to open file: %s", filename.c_str());
            return;
        }

        RCLCPP_INFO(this->get_logger(), "Successfully opened file: %s", filename.c_str());

        std::string line;
        while (std::getline(file, line)) {
            std::stringstream ss(line);
            double x, y, z;
            char comma1, comma2;

            if (ss >> x >> comma1 >> y >> comma2 >> z && comma1 == ',' && comma2 == ',') {
                geometry_msgs::msg::Point point;
                point.x = x;
                point.y = y;
                point.z = z;
                trajectory_.push_back(point);
            } else {
                RCLCPP_WARN(this->get_logger(), "Invalid line format: %s", line.c_str());
            }
        }

        file.close();

        if (trajectory_.empty()) {
            RCLCPP_WARN(this->get_logger(), "Trajectory file is empty or has invalid data.");
        } else {
            RCLCPP_INFO(this->get_logger(), "Loaded %zu trajectory points.", trajectory_.size());
        }
    }

    void publishMarkers() {
        if (trajectory_.empty()) {
            RCLCPP_WARN_THROTTLE(this->get_logger(), *this->get_clock(), 5000, "No trajectory points to publish.");
            return;
        }

        visualization_msgs::msg::MarkerArray marker_array;
        visualization_msgs::msg::Marker marker;
        marker.header.frame_id = "map";
        marker.header.stamp = this->now();
        marker.ns = "trajectory";
        marker.id = 0;  // Required for RViz visualization
        marker.type = visualization_msgs::msg::Marker::SPHERE_LIST;
        marker.action = visualization_msgs::msg::Marker::ADD;
        marker.scale.x = 0.1;
        marker.scale.y = 0.1;
        marker.scale.z = 0.1;
        marker.color.a = 1.0;
        marker.color.r = 1.0;
        marker.points = trajectory_;

        marker_array.markers.push_back(marker);
        marker_publisher_->publish(marker_array);

        RCLCPP_INFO_ONCE(this->get_logger(), "Trajectory markers published.");
    }
};

int main(int argc, char **argv) {
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<TrajectoryReader>());
    rclcpp::shutdown();
    return 0;
}

