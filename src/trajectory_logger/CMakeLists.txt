cmake_minimum_required(VERSION 3.8)
project(trajectory_logger)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(std_srvs REQUIRED)
find_package(rosidl_default_generators REQUIRED)
find_package(rclcpp REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(nav_msgs REQUIRED)
find_package(visualization_msgs REQUIRED)
find_package(tf2_ros REQUIRED)
find_package(tf2_geometry_msgs REQUIRED)
find_package(ament_cmake REQUIRED)

# uncomment the following section in order to fill in
# further dependencies manually.
# find_package(<dependency> REQUIRED)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

rosidl_generate_interfaces(${PROJECT_NAME} "srv/SaveTrajectory.srv")

add_executable(trajectory_publisher src/trajectory_publisher.cpp)
ament_target_dependencies(trajectory_publisher rclcpp geometry_msgs nav_msgs visualization_msgs tf2_ros tf2_geometry_msgs std_srvs)

add_executable(trajectory_reader src/trajectory_reader.cpp)
ament_target_dependencies(trajectory_reader rclcpp geometry_msgs nav_msgs visualization_msgs tf2_ros tf2_geometry_msgs)

ament_export_dependencies(rosidl_default_runtime)

rosidl_get_typesupport_target(cpp_typesupport_target ${PROJECT_NAME} "rosidl_typesupport_cpp")
target_link_libraries(trajectory_publisher ${cpp_typesupport_target})

install(DIRECTORY 
  srv
DESTINATION share/${PROJECT_NAME})

install(TARGETS
  trajectory_publisher
  trajectory_reader
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
