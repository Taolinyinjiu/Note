#import "@preview/obsidius:0.1.1": *

// change the title of the document
#show: notes.with("ROS2 And PX4 Learn Book");

#set text(font: "LXGW WenKai Mono GB");

#set page(margin: 0.7in)

#outline() // 插入目录，通常放在文档开头

#pagebreak() // 目录和正文之间可以加个分页符

= ROS2

== ROS
在提到ROS2之前，我们不得不提到ROS,就像提到C++不得不提到C一样。ROS的全称是Robot Operating System，也被中译为机器人操作系统。但ROS并不像是Windows，Linux，Macos那样的操作系统，而是一个可以安装在现在已有的操作系统上的一个软件库和工具集。

ROS诞生于2007年，它的出现解决了机器人各个组件间的通信问题，同时基于ROS完善的通信机制，越来越多的机器人算法被集成到ROS中。

现在的ROS功能已经变得十分强大，但是随着时代的发展，人们对ROS的期望变得更高，从而催生出了ROS2。ROS2继承了ROS原有的优秀之处，又扩展了新的功能。


== Node
在ROS2中，Node是一个核心概念，他是ROS2计算图中的基本执行单元。

通常一个节点就是一个可以独立运行的可执行程序，就像我们使用g++将cpp源文件编译后得到的可执行文件。节点可以是一个cpp程序，也可以是一个python程序，也可以是其他语言编写的程序。

另外，我们鼓励一个节点只负责一个特定的，模块化的功能：
- 一个节点负责从激光雷达读取数据
- 一个节点负责控制机器人底盘的点击
- 一个节点负责规划机器人运动的路径

上述这些节点，不直接相互调用函数，而是通过ROS提供的通信机制(topic service action parameters)进行交互

== Communiction System

=== Topic

=== Service

=== Action

=== Parameters

== WorkSpace

== Colcon Build

== Software Packages
