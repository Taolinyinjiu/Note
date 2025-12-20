# FastDrone250项目

FastDrone250项目是由高飞老师团队开源的小型自主无人机导航项目，其基于Ego_Planner,VINS,PX4Ctrl三者结合而成。

Ego_Planner : 接收无人机状态，点云数据，局部地图，期望点，输出优化后的轨迹
PX4_Ctrl : 接收优化后的轨迹，将轨迹转换为姿态与推力
VINS: 读取相机数据，基于双目相机与IMU，输出里程计，也可以输出相机的稀疏点云数据or 根据深度图输出稠密的点云数据

## FastDrone250整体框架

> 主要分析源代码src文件夹下

- planner : ego_planner的核心代码，也是论文仓库中的开源代码
- realflight_modules : 实机模块
  - px4ctrl
  - realsense-ros
  - VINS-Fusion
- uav_simulator : 仿真器
  - fake_drone
  - local_sensing
  - map_generator
  - mockamap
  - odom_visualization
  - so3_control
  - so3_quadrotor_simulator
- utils
  - catkin_simple
  - cmake_utils
  - DecompROS
  - pose_utils
  - quadrotor_msgs
  - rviz_plugins
  - uav_utils



### ego_planner singal

    /broadcast_bspline
    /drone_0_ego_planner_node/a_star_list
    /drone_0_ego_planner_node/global_list
    /drone_0_ego_planner_node/goal_point
    /drone_0_ego_planner_node/grid_map/occupancy
    /drone_0_ego_planner_node/grid_map/occupancy_inflate
    /drone_0_ego_planner_node/init_list
    /drone_0_ego_planner_node/optimal_list
    /drone_0_odom_visualization/cmd
    /drone_0_odom_visualization/covariance
    /drone_0_odom_visualization/covariance_velocity
    /drone_0_odom_visualization/height
    /drone_0_odom_visualization/path
    /drone_0_odom_visualization/pose
    /drone_0_odom_visualization/robot
    /drone_0_odom_visualization/sensor
    /drone_0_odom_visualization/trajectory
    /drone_0_odom_visualization/velocity
    /drone_0_pcl_render_node/camera_pose
    /drone_0_pcl_render_node/cloud
    /drone_0_pcl_render_node/depth
    /drone_0_pcl_render_node/local_map
    /drone_0_planning/bspline
    /drone_0_planning/data_display
    /drone_0_planning/pos_cmd
    /drone_0_planning/swarm_trajs
    /drone_0_visual_slam/odom
    /map_generator/global_cloud
    /map_generator/local_cloud
    /pcl_render_node/local_map
    /random_forest/odometry
    /rosout
    /rosout_agg
    /tf
    /traj_start_trigger
    /vins_estimator/extrinsic