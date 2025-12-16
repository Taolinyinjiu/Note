# sunray_simulator

sunray配套模拟器，测试时启动脚本为`sunrat_sim_1uav.launch`，具体内容如下
```xml

<?xml version="1.0"?>
<launch>
        <!-- Gazebo 配置 -->
    <arg name="gazebo_enable" default="true"/>
    <arg name="gui" default="true"/>
    <arg name="world" default="$(find sunray_simulator)/worlds/sunray_empty_world.world"/>
    <!-- 启动 Gazebo -->
    <group if="$(arg gazebo_enable)">
        <include file="$(find gazebo_ros)/launch/empty_world.launch">
            <arg name="world_name" value="$(arg world)"/>
            <arg name="gui" value="$(arg gui)"/>
                        <arg name="use_sim_time" value="false"/>
        </include>
    </group>

    <!-- 无人机配置 -->
    <!-- 无人机模型名称 -->
    <arg name="vehicle" default="sunray150"/>
    <!--无人机编号-->
    <arg name="uav_id" default="1"/>
    <!-- 无人机初始位置 -->
    <arg name="uav_init_x" default="0.0"/>
    <arg name="uav_init_y" default="0.0"/>
    <arg name="uav_init_yaw" default="0.0"/>

    <!-- UAV1 -->
    <include file="$(find sunray_simulator)/launch_basic/sunray_px4_basic.launch">
        <arg name="uav_id" value="$(arg uav_id)" />
        <arg name="vehicle" value="$(arg vehicle)" />
        <arg name="uav_init_x" value="$(arg uav_init_x)"/>
        <arg name="uav_init_y" value="$(arg uav_init_y)"/>
        <arg name="uav_init_yaw" value="$(arg uav_init_yaw)"/>
    </include>
</launch>

```

其中有关uav的具体配置，调用了`sunray_px4_basic.launch`，其具体内容为
```xml

<?xml version="1.0"?>
<launch>
        <!-- 启动 PX4 SITL -->
        <!-- PX4源码中与此相关的文件： -->
        <!-- PX4 SITL rcS启动脚本路径：~/PX4/ROMFS/px4fmu_common/init.d-posix/rcS -->

    <!-- PX4仿真环境变量 -->
    <!-- 对应文件：ROMFS/px4fmu_common/init.d-posix/airframes/10020_gazebo-classic_sunray，可以在这个文件里面更改默认PX4仿真参数 -->
    <env name="PX4_SIM_MODEL" value="gazebo-classic_sunray" />
        <!-- 仿真速度因子 1.0代表与真实时间同步，大于1加快仿真速度，小于1则减慢 （电脑性能较差，可选择减小该参数）-->
        <env name="PX4_SIM_SPEED_FACTOR" value="1.0" />
    <!-- PX4滤波器参数 -->
    <arg name="est" default="ekf2"/>
    <!-- 无人机模型名字 -->
    <arg name="vehicle" default="sunray150"/>

        <!-- 无人机编号说明 -->
        <!-- uav_id为Sunray中对无人机编号的定义，从1开始 -->
        <!-- ID为本文件中对无人机编号的定义，用于标识不同设备或实例的唯一标识符，从0开始 -->
        <!-- MAV_SYS_ID为PX4中无人机编号的定义，在rcS文件中可以发现：MAV_SYS_ID = ID + 1，即从1开始--> 
    <arg name="uav_id" default="1"/>
    <arg name="ID" value="$(eval arg('uav_id') - 1)"/>

    <!-- uav_init_x, uav_init_y, uav_init_z: 无人机的初始位置 -->
    <!-- uav_init_roll, uav_init_pitch, uav_init_yaw: 无人机的初始姿态 -->
    <arg name="uav_init_x" default="0"/>
    <arg name="uav_init_y" default="0"/>
    <arg name="uav_init_z" default="0.2"/>
    <arg name="uav_init_yaw" default="0"/>

    <!-- 
        PX4端端口号说明
        mavlink_id：mavlink_id用于区分无人机
        mavlink_udp_port: MAVLink通信所使用的UDP端口号
        mavlink_tcp_port: MAVLink通信所使用的TCP端口号，mavlink_tcp_port = simulator_tcp_port = 4560 + ID
        SDF文件中的mavlink_tcp_port与rcS文件中的simulator_tcp_port应当一致，并随着无人机编号递增
        mavlink_cam_udp_port: MAVLink相机通信所使用的UDP端口号（不重要）
        gst_udp_port: GStreamer（流媒体处理软件）所使用的UDP端口号（不重要）
        video_uri: 视频流的URI地址（不重要）
    -->
    <arg name="mavlink_id" value="$(eval 1 + arg('ID'))" />
    <arg name="mavlink_udp_port" value="$(eval 14560 + arg('ID'))"/>
    <arg name="mavlink_tcp_port" value="$(eval 4560 + arg('ID'))"/>
    <arg name="mavlink_cam_udp_port" value="$(eval 14530 + arg('ID'))"/>
    <arg name="gst_udp_port" value="$(eval 5600 + arg('ID'))"/>
    <arg name="video_uri" value="$(eval 5600 + arg('ID'))"/>

    <!-- 使用group标签来对不同的无人机进行分组，因此，不同无人机的话题会带上前缀，如/uav0、/uav1等 -->
    <group ns="/uav$(arg uav_id)">
        <!-- 生成无人机SDF模型 -->
        <arg name="cmd" default="$(find sunray_simulator)/scripts/jinja_gen.py --stdout --mavlink_id=$(arg mavlink_id) --mavlink_udp_port=$(arg mavlink_udp_port) 
                                    --mavlink_tcp_port=$(arg mavlink_tcp_port) --gst_udp_port=$(arg gst_udp_port) --video_uri=$(arg video_uri) 
                                    --mavlink_cam_udp_port=$(arg mavlink_cam_udp_port) $(find sunray_simulator)/models/drone_models/$(arg vehicle)/$(arg vehicle).sdf.jinja $(find sunray_simulator)"/>
        <param command="$(arg cmd)" name="sdf_$(arg vehicle)$(arg ID)"/>

        <!-- 启动PX4 SITL -->
        <arg name="interactive" default="true"/>
        <arg unless="$(arg interactive)" name="px4_command_arg1" value=""/>
        <arg     if="$(arg interactive)" name="px4_command_arg1" value="-d"/>
        <node name="px4_sitl_$(arg uav_id)" pkg="px4" type="px4" output="screen" 
            args="$(find px4)/build/px4_sitl_default/etc -s etc/init.d-posix/rcS -i $(arg ID) -w sitl_$(arg vehicle)_$(arg ID) $(arg px4_command_arg1)">
        </node>

        <!-- 加载Gazebo模型 -->
        <node name="$(arg vehicle)_$(arg uav_id)_spawn" pkg="gazebo_ros" type="spawn_model" output="screen" 
            args="-sdf -param sdf_$(arg vehicle)$(arg ID) -model uav$(arg uav_id) -x $(arg uav_init_x) -y $(arg uav_init_y) -z $(arg uav_init_z) -Y $(arg uav_init_yaw)"/>

        <!-- 启动MAVROS -->
        <include file="$(find sunray_simulator)/launch_basic/sunray_mavros_sim.launch">
            <arg name="ID" value="$(arg ID)" />
        </include>
    </group>
</launch>


```

文件中关于mavros的配置引用了文件`sunray_mavros_sim.launch`

``` xml
<?xml version="1.0"?>
<launch>
    <!-- vehicle model and world -->
    <arg name="ID" default="0"/>

    <!-- 
        Mavros端端口号说明
        udp_port_local: 用于PX4与Mavros进行UDP通信的本地端口号，udp_port_local = 14580 + ID
        udp_port_remote: 用于PX4与Mavros进行UDP通信的远程端口号，udp_port_remote = 14540 + ID
        fcu_url: 定义PX4飞控单元的统一资源定位符（URL），包括UDP端口和主机地址等信息。
    -->
        <arg name="udp_port_local" value="$(eval 14580 + arg('ID'))"/>
    <arg name="udp_port_remote" value="$(eval 14540 + arg('ID'))"/>
    <arg name="fcu_url" default="udp://:$(arg udp_port_remote)@localhost:$(arg udp_port_local)"/>
    <arg name="gcs_url" default="" />
    <arg name="respawn_mavros" default="false" />

    <!-- 启动MAVROS -->
    <node pkg="mavros" type="mavros_node" name="mavros" output="screen" launch-prefix="bash -c 'sleep 8; $0 $@'">
        <param name="fcu_url" value="$(arg fcu_url)" />
        <param name="gcs_url" value="$(arg gcs_url)" />
        <param name="target_system_id" value="$(eval 1 + arg('ID'))"/>
        <param name="target_component_id" value="1" />
        <param name="fcu_protocol" value="v2.0" />
        <rosparam command="load" file="$(find sunray_simulator)/config/px4_config.yaml" />
        <rosparam command="load" file="$(find sunray_simulator)/config/px4_pluginlists.yaml" />
    </node>
</launch>

```
注意到此处是对mavros进行了重映射，并且我们没有使用sunray的自定义消息UAVState，而是是使用的mavros

uav可以在gazebo中使用外部定位，定位源可以选择从gazebo中获得，起飞降落demo的脚本如下:
```bash
#!/bin/bash
# 脚本：起飞降落demo
gnome-terminal --window -e 'bash -c "roscore; exec bash"' \
--tab -e 'bash -c "sleep 2.0; roslaunch sunray_simulator sunray_sim_1uav.launch; exec bash"' \
--tab -e 'bash -c "sleep 2.0; roslaunch sunray_uav_control external_fusion.launch external_source:=2 enable_rviz:=true; exec bash"' \
--tab -e 'bash -c "sleep 2.0; roslaunch sunray_uav_control sunray_control_node.launch uav_id:=1; exec bash"' \

gnome-terminal --window -e  'bash -c "sleep 2.0; roslaunch sunray_tutorial run_demo.launch demo_id:=1 uav_id:=1; exec bash"' \
```
analyse:
1. 启动roscore
2. 启动sunray_simulator 仿真器，选择1个无人机进行仿真测试
3. 设置uav定位方式为外部定位，选择定位源为gazebo
4. 启动无人机控制节点`sunray_control_node`，跟随无人机编号`uav_id`
5. 解锁无人机，运行`roslaunch sunray_tutorial run_demo.launch demo_id:=1 uav_id:=1`


sunray_formation 总是会构建失败



## sunray_uav_control external_fusion.launch

``` xml
<launch>
    <!-- ODOM = 0, POSE = 1, GAZEBO = 2,  MOCAP = 3, VIOBOT = 4, GPS = 5, RTK = 6, VINS = 7 -->
    <arg name="uav_id" default="1" />
    <arg name="external_source" default="4" />
    <arg name="uav_name" default="uav" />
    <arg name="position_topic" default="/Odometry" />
    <arg name="enable_rviz" default="false" />
    <arg name="enable_range_sensor" default="false" />
    <!-- 是否使用vision_pose话题至PX4，false:直接使用Mavlink发送外部定位数据到PX4 -->
    <arg name="use_vision_pose" default="true" />
    <arg name="server" default="192.168.20.15"/>
    <arg name="tilted" default="false"/>
    

    <!-- 启动 external_fusion_node-->
    <node name="external_fusion" pkg="sunray_uav_control" type="external_fusion_node" output="screen">
        <param name="uav_id" value="$(arg uav_id)" />
        <param name="external_source" value="$(arg external_source)" />
        <param name="uav_name" value="$(arg uav_name)" />
        <param name="position_topic" value="$(arg position_topic)" />
        <param name="enable_range_sensor" value="$(arg enable_range_sensor)" />
        <param name="use_vision_pose" value="$(arg use_vision_pose)" />
        <param name="tilted" value="$(arg tilted)" />
    </node>

    <!-- 启动 vrpn_client_ros -->
    <include file="$(find sunray_uav_control)/launch/sunray_vrpn.launch" if="$(eval external_source == 3)">
        <arg name="server" value="$(arg server)"/>
        <arg name="uav_id" value="$(arg uav_id)"/>
    </include>

    <arg name="rivz_config" default="$(find sunray_uav_control)/rviz/uav.rviz"/>
        <!-- 启动Rviz-->
        <group if="$(arg enable_rviz)">
        <node type="rviz" name="rviz_external_fusion" pkg="rviz" args="-d $(arg rivz_config)"/>
    </group>
</launch>
```


## sunray_uav_control sunray_control_node.launch

```xml
<launch>
    <arg name="uav_id" default="1" />
    <arg name="uav_name" default="uav" />
    <arg name="x_min" default="-20.0" />
    <arg name="x_max" default="20.0" />
    <arg name="y_min" default="-20.0" />
    <arg name="y_max" default="20.0" />
    <arg name="z_min" default="-20.0" />
    <arg name="z_max" default="20.0" />
    <arg name="land_type" default="0" />
    <arg name="land_end_time" default="1.0" />
    <arg name="land_end_speed" default="0.3" />
    <arg name="Takeoff_height" default="0.6" />
    <arg name="Disarm_height" default="0.2" />
    <arg name="Land_speed" default="0.1" />
    <arg name="home_x" default="0.0" />
    <arg name="home_y" default="0.0" />
    <arg name="home_z" default="0.0" />
    <arg name="home_yaw" default="0.0" />
    <arg name="use_rc_control" default="false" />
    <arg name="check_flip" default="true" />
    <arg name="check_cmd_timeout" default="false" />
    <arg name="cmd_timeout" default="5.0" />
    <arg name="use_offset" default="false" />

    <!-- 启动 uav_control_node -->
    <node name="uav_control" pkg="sunray_uav_control" type="uav_control_node" output="screen">
        <param name="uav_id" value="$(arg uav_id)" />
        <param name="uav_name" value="$(arg uav_name)" />
        <!-- 起飞高度 | 降落第一阶段高度 | 降落速度 -->
        <!-- 降落模式 1：调用px4 auto.land 其他：指定高度锁桨 -->
        <param name="flight_params/Takeoff_height" value="$(arg Takeoff_height)" />
        <param name="flight_params/land_type" value="$(arg land_type)" />
        <param name="flight_params/Disarm_height" value="$(arg Disarm_height)" />
        <param name="flight_params/Land_speed" value="$(arg Land_speed)" />
        <!-- 降落最后一阶段需要的时间和速度 -->
        <param name="flight_params/land_end_time" value="$(arg land_end_time)" />
        <param name="flight_params/land_end_speed" value="$(arg land_end_speed)" />
        <!-- 默认home点 -->
        <param name="flight_params/home_x" value="$(arg home_x)" />
        <param name="flight_params/home_y" value="$(arg home_y)" />
        <param name="flight_params/home_z" value="$(arg home_z)" />
        <!-- 安全围栏 超出会降落 -->
        <param name="geo_fence/x_min" value="$(arg x_min)" />
        <param name="geo_fence/x_max" value="$(arg x_max)" />
        <param name="geo_fence/y_min" value="$(arg y_min)" />
        <param name="geo_fence/y_max" value="$(arg y_max)" />
        <param name="geo_fence/z_min" value="$(arg z_min)" />
        <param name="geo_fence/z_max" value="$(arg z_max)" />
        <!-- 是否使用遥控器控制 如果不使用则不允许进入RC_CONTROL模式，允许在解锁前切换到offboard模式再解锁-->
        <param name="system_params/use_rc_control" value="$(arg use_rc_control)" />
        <!-- 是否检测指令超时 允许两条指令之间的时长 超时后进入悬停-->
        <param name="system_params/check_cmd_timeout" value="$(arg check_cmd_timeout)" />
        <param name="system_params/cmd_timeout" value="$(arg cmd_timeout)" />
        <!-- 定位超时警告和降落时间 -->
        <param name="system_params/odom_valid_timeout" value="0.5" />
        <param name="system_params/odom_valid_warming_time" value="0.3" />
        <!-- 是否加上初始偏移 只对NED的位置控制有效 解锁位置设置为原点(0,0,0) 适用于GPS或RTK模式 -->
        <param name="system_params/use_offset" value="$(arg use_offset)" />
        <!--翻转上锁-->
        <param name="system_params/check_flip" value="$(arg check_flip)" />
        <!-- 姿态控制参数 -->
        <param name="ctrl_param/quad_mass" value="1.0" />
        <param name="ctrl_param/hov_percent" value="0.37" />
        <param name="ctrl_param/pxy_int_max" value="10.0" />
        <param name="ctrl_param/pz_int_max" value="10.0" />
        <param name="ctrl_param/Kp_xy" value="3.0" />
        <param name="ctrl_param/Kp_z" value="3.0" />
        <param name="ctrl_param/Kv_xy" value="3.0" />
        <param name="ctrl_param/Kv_z" value="3.0" />
        <param name="ctrl_param/Kvi_xy" value="0.3" />
        <param name="ctrl_param/Kvi_z" value="0.3" />
        <param name="ctrl_param/tilt_angle_max" value="20.0" />
    </node>

```

## Sunray/General_Module/sunray_tutorial/launch/run_demo.launch

```xml

<launch>
        <arg name="uav_id" default="1"/>
    <arg name="uav_name" default="uav" />
    <arg name="demo_id" default="1" />
    
        <node if="$(eval demo_id == 1)" pkg="sunray_tutorial" type="takeoff_hover_land" name="takeoff_hover_land_$(arg uav_id)" output="screen">
                <param name="uav_id" value="$(arg uav_id)" />
                <param name="uav_name" value="$(arg uav_name)" />
        </node>

        <node if="$(eval demo_id == 2)" pkg="sunray_tutorial" type="block_xyzpos" name="block_xyzpos_$(arg uav_id)" output="screen">
                <param name="uav_id" value="$(arg uav_id)" />
                <param name="uav_name" value="$(arg uav_name)" />
        </node>

        <node if="$(eval demo_id == 3)" pkg="sunray_tutorial" type="circle_xyzvel" name="circle_xyzvel_$(arg uav_id)" output="screen">
                <param name="uav_id" value="$(arg uav_id)" />
                <param name="uav_name" value="$(arg uav_name)" />
        </node>

        <node if="$(eval demo_id == 4)" pkg="sunray_tutorial" type="circle_xyvelzpos" name="circle_xyvelzpos_$(arg uav_id)" output="screen">
                <param name="uav_id" value="$(arg uav_id)" />
                <param name="uav_name" value="$(arg uav_name)" />
        </node>

        <node if="$(eval demo_id == 5)" pkg="sunray_tutorial" type="hexagon_xyzposyawbody" name="pos_body_hexagon_$(arg uav_id)" output="screen">
                <param name="uav_id" value="$(arg uav_id)" />
                <param name="uav_name" value="$(arg uav_name)" />
        </node>

        <node if="$(eval demo_id == 6)" pkg="sunray_tutorial" type="vel_body_follow_car" name="vel_body_follow_car_$(arg uav_id)" output="screen">
                <param name="uav_id" value="$(arg uav_id)" />
                <param name="uav_name" value="$(arg uav_name)" />
        </node>

        <node if="$(eval demo_id == 7)" pkg="sunray_tutorial" type="vel_body_z_pos_follow_car" name="vel_body_z_pos_follow_car_$(arg uav_id)" output="screen">
                <param name="uav_id" value="$(arg uav_id)" />
                <param name="uav_name" value="$(arg uav_name)" />
        </node>
        
        <!-- <node pkg="sunray_tutorial" type="follow_car_xyvelzposyawbody" name="follow_a_car_$(arg uav_id)" output="screen">
                <param name="uav_id" value="$(arg uav_id)" />
                <param name="uav_name" value="$(arg uav_name)" />
        </node> -->
</launch>

```


## takeoff_hover_land.cpp

```cpp

/*
    起飞降落例程：takeoff_hover_land.cpp
    程序功能：自动起飞、指定点悬停、自动降落
*/

#include "ros_msg_utils.h"

int uav_id;
string node_name;
string uav_name;
sunray_msgs::UAVState uav_state;
sunray_msgs::UAVSetup uav_setup;
sunray_msgs::UAVControlCMD uav_cmd;

void mySigintHandler(int sig)
{
    std::cout << "[takeoff_hover_land] exit..." << std::endl;

    ros::shutdown();
    exit(EXIT_SUCCESS); // 或者使用 exit(0)
}

// 无人机状态回调
void uav_state_callback(const sunray_msgs::UAVState::ConstPtr &msg)
{
    uav_state = *msg;
}

int main(int argc, char **argv)
{
    // 设置日志
    Logger::init_default();

    ros::init(argc, argv, "takeoff_hover_land");
    ros::NodeHandle nh("~");
    ros::Rate rate(20.0);

    signal(SIGINT, mySigintHandler);

    node_name = ros::this_node::getName();
    node_name = "["+node_name+"]:";

    // 【参数】无人机编号
    nh.param<int>("uav_id", uav_id, 1);
    // 【参数】无人机名称
    nh.param<string>("uav_name", uav_name, "uav");
    uav_name = "/" + uav_name + std::to_string(uav_id);

    // 【订阅】无人机状态
    ros::Subscriber uav_state_sub = nh.subscribe<sunray_msgs::UAVState>(uav_name + "/sunray/uav_state", 10, uav_state_callback);
    // 【发布】无人机控制指令 （本节点 -> sunray_control_node）
    ros::Publisher control_cmd_pub = nh.advertise<sunray_msgs::UAVControlCMD>(uav_name + "/sunray/uav_control_cmd", 1);
    // 【发布】无人机设置指令（本节点 -> sunray_control_node）
    ros::Publisher uav_setup_pub = nh.advertise<sunray_msgs::UAVSetup>(uav_name + "/sunray/setup", 1);

    // 控制辅助类 - 初始化
    Control_Utils uav_control_utils;
    uav_control_utils.init(nh, uav_id, node_name);

    // 初始化检查：等待PX4连接
    int times = 0;
    while (ros::ok() && !uav_state.connected)
    {
        ros::spinOnce();
        ros::Duration(1.0).sleep();
        if (times++ > 5)
            Logger::print_color(int(LogColor::red), node_name, "Wait for UAV connect...");
    }

    // 控制辅助类 - 自动起飞
    uav_control_utils.auto_takeoff();

    // 以上: 无人机已成功起飞，进入自由任务模式
    Logger::print_color(int(LogColor::green), node_name, "Wait 5 sec and then send Hover cmd...");

    ros::Duration(5.0).sleep();
    // 发布悬停指令
    Logger::print_color(int(LogColor::green), node_name, "Send UAV Hover cmd.");
    uav_cmd.header.stamp = ros::Time::now();
    uav_cmd.cmd = sunray_msgs::UAVControlCMD::Hover;
    control_cmd_pub.publish(uav_cmd);
    ros::Duration(5).sleep();
    ros::spinOnce();

    Logger::print_color(int(LogColor::green), node_name, "Wait 5 sec and then send Land cmd...");
    ros::Duration(5.0).sleep();

    // 控制辅助类 - 自动降落
    uav_control_utils.auto_land();

    // Demo 结束
    Logger::print_color(int(LogColor::green), node_name, "Demo finished, quit!");
    
    return 0;
}

```