当前任务:将VINS与Sunray项目结合，首先在仿真环境中实现基于VINS里程计的定位飞行，然后尝试使用推力-姿态控制接口，底层为Sunray系列的PID控制器。

### 12.7
- 完成vins-fusion的编译工作，测试在gazebo中vins工作良好，测试模型为sunray150_mid360_d435，测试场景为cafe.world
TODO：阅读fastdrone250项目结构，观察中间件px4ctrl如何替换为sunray接口，或者根据px4ctrl改写sunray控制接口  

### 12.8
- 编写一键启动脚本，并入Robot_Publiser模型描述节点

```xml
<launch>
  <param name="robot_description" 
         command="$(find xacro)/xacro '$(find sunray_simulator)/models/drone_models/sunray150_D435i/sunray150_D435i.xacro'" />

  <node name="robot_state_publisher" pkg="robot_state_publisher" type="robot_state_publisher" />

  <node name="joint_state_publisher" pkg="joint_state_publisher" type="joint_state_publisher" />

  </launch>
```

一共有三个imu来源，分别是uav/mavros，/livox/imu，/camera/imu，静止状态下截取三帧数据
/camera/imu
header: 
  seq: 12260
  stamp: 
    secs: 199
    nsecs: 612000000
  frame_id: "D435i::imu_link"
orientation: 
  x: -0.00019227876354010432
  y: 0.00018048890555440707
  z: 0.7068249099039658
  w: 0.7073884909947876
orientation_covariance: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
angular_velocity: 
  x: 2.5084631023758256e-05
  y: 2.7098529076929268e-06
  z: 4.489522048117583e-09
angular_velocity_covariance: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
linear_acceleration: 
  x: -0.005166230292105087
  y: -0.00016553783495697126
  z: 9.799998635595081
linear_acceleration_covariance: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
---

/uav/mavros/imu
header: 
  seq: 9808
  stamp: 
    secs: 197
    nsecs: 530000000
  frame_id: "base_link"
orientation: 
  x: 1.564767605426282e-05
  y: -0.021327804852356972
  z: -0.743011923777357
  w: -0.668938268537006
orientation_covariance: [1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0]
angular_velocity: 
  x: 0.000963602855335921
  y: -0.0039391410537064075
  z: -0.0020633740350604053
angular_velocity_covariance: [1.2184696791468346e-07, 0.0, 0.0, 0.0, 1.2184696791468346e-07, 0.0, 0.0, 0.0, 1.2184696791468346e-07]
linear_acceleration: 
  x: -0.3683072328567505
  y: 0.38920465111732605
  z: 9.853507041931152
linear_acceleration_covariance: [8.999999999999999e-08, 0.0, 0.0, 0.0, 8.999999999999999e-08, 0.0, 0.0, 0.0, 8.999999999999999e-08]
---

/uav/livox/imu
header: 
  seq: 2216
  stamp: 
    secs: 197
    nsecs: 948000000
  frame_id: "livox_mid360::base_link"
orientation: 
  x: -0.00019666411238467425
  y: 0.00018486343295282852
  z: 0.7068251630168388
  w: 0.7073882357482045
orientation_covariance: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
angular_velocity: 
  x: -8.48906332973897e-08
  y: 2.709880480994756e-06
  z: 2.13973037677057e-10
angular_velocity_covariance: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
linear_acceleration: 
  x: -0.005287636269540556
  y: -0.00016565431510070212
  z: 9.799998572115673
linear_acceleration_covariance: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
---

