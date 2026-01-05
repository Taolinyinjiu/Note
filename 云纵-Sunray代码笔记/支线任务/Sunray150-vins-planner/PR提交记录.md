# 向主仓库Sunray线提交PR

首先从Gitee同步最新的Sunray主线，然后明确本次涉及的部分为
- 添加VINS软件包[x]
- 添加VINS仿真环境，主要为awa系列的gazebo仿真环境[x]
- 添加VINS仿真脚本，机器人模型在RVIZ中正常显示，修正TF树[x]
- 添加VINS实机脚本，支持一键起飞
- 添加VINS调试脚本，一键录制rosbag
- 对external_fusion.launch sunray_control_node.launch terminal_control.launch三个launch文件添加launch-prefix参数，用于在脚本中新开终端实现控制


<!-- 启动控制节点 -->
<arg name="enable_control" default="false"/>
<group if="$(arg enable_control)">
<include file="$(find sunray_uav_control)/launch/sunray_control_node.launch"></include>
<!-- 设置px4飞控的定位源 -->
<include file="$(find sunray_uav_control)/launch/external_fusion.launch">
        <!-- external_source = 2: Gazebo 真直，调试用  0: vins里程计的odom作为定位的odom -->
        <!-- <arg name="external_source" value="2" /> -->
        <arg name="external_source" value="0" /> 
        <arg name="position_topic" value="/vins_estimator/odometry" />

</include>
<!-- 设置为终端控制 -->
<include file="$(find sunray_uav_control)/launch_utils/terminal_control.launch">
</include>
</group>