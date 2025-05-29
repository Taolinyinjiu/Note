# Gazebo plugins in ROS - Tutorial: Using Gazebo plugins with ROS
> Gazebo plugins give your URDF models greater functionality and can tie in ROS messages and service calls for sensor output and motor input. In this tutorial we explain both how to setup preexisting plugins and how to create your own custom plugins that can work with ROS.
>
> Gazebo 插件是增强机器人 URDF 模型在仿真环境中功能性的关键工具。它们不仅能让模型拥有感知和运动的能力，更重要的是，通过与 ROS 消息和服务调用的集成，Gazebo 仿真环境可以成为一个与真实的 ROS 机器人系统高度相似的开发和测试平台。开发者可以利用预先存在的插件快速搭建仿真场景，也可以根据自己的需求创建自定义插件，实现特定的传感器模拟和电机控制，并方便地将仿真数据和控制逻辑与 ROS 生态系统中的其他组件连接起来。这对于机器人算法的开发、测试和验证来说至关重要。
 
##  Prerequisites
Make sure you have the RRBot setup as described in the previous tutorial on URDFs. Also make sure you have understood the use of the <gazebo> element within the URDF description, from that same tutorial.

确保你已经了解了有关于URDF的知识，并且理解<gazebo>元素同URDF中的描述是相似的教程

## Plugin Types
Gazebo supports several plugin types, and all of them can be connected to ROS, but only a few types can be referenced through a URDF file:
Gazebo 架构允许开发者创建不同类型的插件，以扩展其在仿真方面的功能。虽然所有的gazebo插件都能连接 ROS，但只有特定的几种插件类型可以直接在 URDF 文件中进行配置和引用。

> URDF 主要用于描述机器人的结构和简单的感知属性。


1. ModelPlugins, to provide access to the physics::Model API 用于控制机器人的物理行为和运动。
2. SensorPlugins, to provide access to the sensors::Sensor API 用于模拟各种传感器并将感知数据发布到 ROS。
3. VisualPlugins, to provide access to the rendering::Visual API 用于增强机器人的可视化效果。


## Adding a ModelPlugin
In short, the ModelPlugin is inserted in the URDF inside the <robot> element. It is wrapped with the <gazebo> pill, to indicate information passed to Gazebo. For example:
当您想在您的机器人模型中添加一个 ModelPlugin 以控制其物理行为或与环境互动时，您需要在 URDF 文件的 <robot> 标签内部添加一个 <gazebo> 标签。在这个 <gazebo> 标签内部，您将配置您的 ModelPlugin，包括指定插件的名称 (name)、包含插件代码的共享库文件 (filename)，以及其他插件所需的参数。例如:
```xml
<robot>
  ... robot description ...
  <gazebo>
    <plugin name="differential_drive_controller" filename="libdiffdrive_plugin.so">
      ... plugin parameters ...
    </plugin>
  </gazebo>
  ... robot description ...
</robot>
```
Upon loading the robot model within Gazebo, the diffdrive_plugin code will be given a reference to the model itself, allowing it to manipulate it. Also, it will be give a reference to the SDF element of itself, in order to read the plugin parameters passed to it.

当 Gazebo 仿真器加载包含 diffdrive_plugin 配置的机器人模型时,Gazebo 会将加载的机器人模型对象的一个引用（类似于指针或句柄）传递给 diffdrive_plugin 的代码。此外，Gazebo 还会向 diffdrive_plugin 提供对其自身在 SDF文件中对应的 XML 元素的引用。即使插件是在 URDF 中配置的，Gazebo 在加载时也会将其转换为 SDF 格式。

这样做的目的是让 diffdrive_plugin 能够读取在 URDF（通过 <gazebo><plugin>...</plugin></gazebo> 标签）或直接在 SDF 文件中为该插件配置的参数。这些参数可以控制插件的行为，例如轮子半径、轮子间距、电机控制参数、发布的 ROS 话题名称等等。

## Adding a SensorPlugin
Specifying sensor plugins is slightly different. Sensors in Gazebo are meant to be attached to links, so the <gazebo> element describing that sensor must be given a reference to that link. For example:

指定传感器插件略有不同。凉亭中的传感器应与链接相连，因此<gazebo>描述该传感器的元素必须给出该链接的引用。例如

```xml
<robot>
  ... robot description ...
  <link name="sensor_link">
    ... link description ...
  </link>

  <gazebo reference="sensor_link">
    <sensor type="camera" name="camera1">
      ... sensor parameters ...
      <plugin name="camera_controller" filename="libgazebo_ros_camera.so">
        ... plugin parameters ..
      </plugin>
    </sensor>
  </gazebo>

</robot>

```

Upon loading the robot model within Gazebo, the camera_controller code will be given a reference to the sensor, providing access to its API. Also, it will be give a reference to the SDF element of itself, in order to read the plugin parameters passed to it.

指的是当 Gazebo 仿真器加载包含 camera_controller 配置的机器人模型时，并且该模型包含一个或多个相机传感器, Gazebo 会将它所管理的相机传感器对象的一个引用传递给 camera_controller 的代码.
意味着通过获得的传感器引用，camera_controller 能够访问相机传感器的 API，从而控制相机的属性（例如分辨率、帧率、视野）、获取相机在仿真过程中捕获的图像数据，并可能将这些数据发布为 ROS 消息。 此外，Gazebo 还会向 camera_controller 提供对其自身在 SDF 文件中对应的 XML 元素的引用。这样做的目的是让 camera_controller 能够读取在 URDF（通过 <gazebo><plugin>...</plugin></gazebo> 标签）或直接在 SDF 文件中为该插件配置的参数。这些参数可以控制相机控制器的行为，例如发布的 ROS 话题名称、图像数据的格式、更新频率等等。

## Plugins available in gazebo_plugins

The following sections document all of the plugins available in the gazebo_plugins.

表明接下来的文档将详细介绍 gazebo_plugins 这个 ROS 包中提供的所有 Gazebo 插件。

We suggest you review them in order 

建议用户按照文档的顺序阅读各个插件的说明。

because more detail is covered in the first couple of plugins 

因为文档的前几个插件可能会更详细地介绍一些基础概念和通用的配置方法

and you can learn some of the concepts from the various plugins' documentation.

不同的插件展示了如何访问不同的 Gazebo API (例如 physics::Model, sensors::Sensor, rendering::Visual) 以及如何与 ROS 集成。


The names of each section is derived from the plugin class name. 

说明文档中每个插件的章节标题都来自于该插件的 C++ 类名。

For example, "Block Laser" is from the GazeboRosBlockLaser class and can be found in the file gazebo_plugins/src/gazebo_ros_block_laser.cpp.

举例说明，名为 "Block Laser" 的文档章节对应于 GazeboRosBlockLaser 这个 C++ 类,该类的源代码文件位于 gazebo_plugins/src/ 目录下，文件名为 gazebo_ros_block_laser.cpp。

If there are some sections blank, 

如果部分文档存在空白

it means that this author got tired of documenting every plugin 

这意味着作者没有完成所有插件的编写工作

and you should fill in the area with your experience should you have knowledge and examples of how to use the particular plugin.

如果用户对某个空白的插件有使用经验和示例，应该贡献自己的知识，帮助其他用户。

## Plugins

### Camera
Description: provides ROS interface for simulating cameras such as wge100_camera by publishing the CameraInfo and Image ROS messages as described in sensor_msgs.

gazebo_ros_camera 插件是 Gazebo 中模拟相机与 ROS 系统进行交互的关键组件。它使得在 Gazebo 中创建的虚拟相机能够像真实的 ROS 相机节点一样工作，将捕获到的图像数据以及相关的相机参数信息以标准的 sensor_msgs/CameraInfo 和 sensor_msgs/Image ROS 消息的形式发布到 ROS 网络中。

**RRBot Example**

In this section, we will review a simple RGB camera attached to the end of the RRBot pendulum arm. You can look inside rrbot.xacro to follow the explanation. The first elements of this block are an extra link and joint added to the URDF file that represents the camera. We are just using a simple red box to represent the camera, though typically you could use a mesh file for a better representation.

在这一节中，我们会提到RGB相机，并在RRBot手臂的末端添加一个相机，想要做到这一点，需要在 URDF 中增加一个新的连杆 (link) 和关节 (joint)，并且可以使用一个简单的几何形状（例如红色的盒子）来表示相机的视觉外观，尽管更真实地表示通常会使用网格 (mesh) 文件。

```xml
  <joint name="camera_joint" type="fixed">
    <axis xyz="0 1 0" />
    <origin xyz="${camera_link} 0 ${height3 - axel_offset*2}" rpy="0 0 0"/>
    <parent link="link3"/>
    <child link="camera_link"/>
  </joint>

  <!-- Camera -->
  <link name="camera_link">
    <collision>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <geometry>
    <box size="${camera_link} ${camera_link} ${camera_link}"/>
      </geometry>
    </collision>

    <visual>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <geometry>
    <box size="${camera_link} ${camera_link} ${camera_link}"/>
      </geometry>
      <material name="red"/>
    </visual>

    <inertial>
      <mass value="1e-5" />
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <inertia ixx="1e-6" ixy="0" ixz="0" iyy="1e-6" iyz="0" izz="1e-6" />
    </inertial>
  </link>
```

A Xacro property is also defined:

```xml

<xacro:property name="camera_link" value="0.05" /> <!-- Size of square 'camera' box -->

```
You should be able to launch the RRBot and see a red box attached to the end of the arm.
您应该能够启动RRBot并看到一个连接到手臂末端的红色框。

Next we will review the Gazebo plugin that gives us the camera functionality and publishes the image to a ROS message. In the RRBot we have been following the convention of putting Gazebo elements in the rrbot.gazebo file:
接下来，我们将回顾Gazebo插件，它为我们提供了相机功能并将图像发布到ROS消息。在RRBot中，我们一直遵循在RRBot中放置Gazebo元素的惯例。rrbot.gazebo文件:

```xml
<!-- camera -->
  <gazebo reference="camera_link">
    <sensor type="camera" name="camera1">
      <update_rate>30.0</update_rate>
      <camera name="head">
        <horizontal_fov>1.3962634</horizontal_fov>
        <image>
          <width>800</width>
          <height>800</height>
          <format>R8G8B8</format>
        </image>
        <clip>
          <near>0.02</near>
          <far>300</far>
        </clip>
        <noise>
          <type>gaussian</type>
          <!-- Noise is sampled independently per pixel on each frame.
               That pixel's noise value is added to each of its color
               channels, which at that point lie in the range [0,1]. -->
          <mean>0.0</mean>
          <stddev>0.007</stddev>
        </noise>
      </camera>
      <plugin name="camera_controller" filename="libgazebo_ros_camera.so">
        <alwaysOn>true</alwaysOn>
        <updateRate>0.0</updateRate>
        <cameraName>rrbot/camera1</cameraName>
        <imageTopicName>image_raw</imageTopicName>
        <cameraInfoTopicName>camera_info</cameraInfoTopicName>
        <frameName>camera_link</frameName>
        <hackBaseline>0.07</hackBaseline>
        <distortionK1>0.0</distortionK1>
        <distortionK2>0.0</distortionK2>
        <distortionK3>0.0</distortionK3>
        <distortionT1>0.0</distortionT1>
        <distortionT2>0.0</distortionT2>
      </plugin>
    </sensor>
  </gazebo>
```
Let's discuss some of the properties of this plugin...
```xml
<gazebo reference="camera_link">
```
The link name "camera_link" must match the name of the link we added to the Xacro URDF.

```xml
<sensor type="camera" name="camera1">
```
The sensor name "camera1" must be unique from all other sensor names. The name is not used many places except for within Gazebo plugins you can access
```xml
<update_rate>30.0</update_rate>
```
Number of times per second a new camera image is taken within Gazebo. This is the maximum update rate the sensor will attempt during simulation but it could fall behind this target rate if the physics simulation runs faster than the sensor generation can keep up.
```xml
<horizontal_fov>1.3962634</horizontal_fov>
<image>
    <width>800</width>
    <height>800</height>
    <format>R8G8B8</format>
</image>
<clip>
    <near>0.02</near>
    <far>300</far>
</clip>
```
Fill in these values to match the manufacturer's specs on your physical camera hardware. One thing to note is that the pixels are assumed to be square.

Additionally, the near and far clips are simulation-specific parameters that give an upper and lower bound to the distance in which the cameras can see objects in the simulation. This is specified in the camera's optometry frame.