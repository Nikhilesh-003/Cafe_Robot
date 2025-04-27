#include "rclcpp/rclcpp.hpp"
#include "std_srvs/srv/trigger.hpp"
#include "visualization_msgs/msg/marker_array.hpp"
#include <fstream>
#include <vector>

using namespace std::chrono_literals;

class TrajectoryRecorder : public rclcpp::Node {
public:
    TrajectoryRecorder() : Node("trajectory_recorder") {
        trajectory_sub_ = this->create_subscription<visualization_msgs::msg::MarkerArray>(
            "/slam_toolbox/graph_visualization", 10, 
            std::bind(&TrajectoryRecorder::trajectory_callback, this, std::placeholders::_1));

        save_service_ = this->create_service<std_srvs::srv::Trigger>(
            "save_trajectory", 
            std::bind(&TrajectoryRecorder::save_trajectory, this, std::placeholders::_1, std::placeholders::_2));
    }

private:
    struct TrajectoryPoint {
        rclcpp::Time timestamp;
        double x;
        double y;
        double z;
    };

    std::vector<TrajectoryPoint> trajectory_;

    void trajectory_callback(const visualization_msgs::msg::MarkerArray::SharedPtr msg) {
        auto now = this->get_clock()->now();
        for (const auto &marker : msg->markers) {
            TrajectoryPoint point;
            point.timestamp = now;
            point.x = marker.pose.position.x;
            point.y = marker.pose.position.y;
            point.z = marker.pose.position.z;
            trajectory_.push_back(point);
        }
    }

    void save_trajectory(const std::shared_ptr<std_srvs::srv::Trigger::Request> request,
                         std::shared_ptr<std_srvs::srv::Trigger::Response> response) {
        (void) request;  // Unused parameter

        double duration = 10.0; // Set duration in seconds (can be modified to take input)
        auto now = this->get_clock()->now();

        std::vector<TrajectoryPoint> filtered_trajectory;
        for (const auto &point : trajectory_) {
            double time_diff = (now - point.timestamp).seconds();
            if (time_diff <= duration) {
                filtered_trajectory.push_back(point);
            }
        }

        if (filtered_trajectory.empty()) {
            response->success = false;
            response->message = "No trajectory data within the specified duration.";
            return;
        }

        save_to_csv("trajectory.csv", filtered_trajectory);

        response->success = true;
        response->message = "Trajectory saved in CSV format.";
    }

    void save_to_csv(const std::string &filename, const std::vector<TrajectoryPoint> &trajectory) {
        std::ofstream file(filename);
        if (!file.is_open()) {
            RCLCPP_ERROR(this->get_logger(), "Failed to open file: %s", filename.c_str());
            return;
        }

        file << "timestamp,x,y,z\n";
        for (const auto &point : trajectory) {
            file << point.timestamp.seconds() << "," << point.x << "," << point.y << "," << point.z << "\n";
        }

        file.close();
        RCLCPP_INFO(this->get_logger(), "Trajectory saved to %s", filename.c_str());
    }

    rclcpp::Subscription<visualization_msgs::msg::MarkerArray>::SharedPtr trajectory_sub_;
    rclcpp::Service<std_srvs::srv::Trigger>::SharedPtr save_service_;
};

int main(int argc, char **argv) {
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<TrajectoryRecorder>());
    rclcpp::shutdown();
    return 0;
}