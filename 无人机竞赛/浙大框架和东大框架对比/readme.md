## ego_planner

首先，通过对planner文件夹的分析来看，东大REAL-DRONE-400和浙大Fast-Drone-250的不同之处在于single_run_in_exp.launch
在这个文件中，浙大里程计使用的是/vins_fusion/imu_propagate，而东大使用的是/Odom_high_freq
换句话说，浙大使用vins进行定位，东大使用fastlio结合imu预积分，输出高频里程计

其次，在26行对于点云话题的参数，浙大使用的是nouse2，也就是不使用点云，而东大使用的是/cloud_registered

接着在最大速度和加速度方面，浙大加速度相对激进，东大比较保守

## px4ctrl

px4ctrl作为ego的底层控制器，通过接受轨迹规划服务器出来的点，执行无人机的运动

两个框架中，px4ctrl的底层没有变化，在launch文件和yaml配置文件中略微有所变化

首先东大的mass设置为2.67kg，起飞高度为0.5m, 悬停油门为0.35，其次PID增益参数为2.0 2.0 2.0

其次在run_ctrl.launch文件中，东大重映射里程计话题为/Odom_high_freq，浙大为/vins_fusion/imu_propagate

因此总结，东大框架整体和浙大重合，只是定位方式由vins转换为了fastlio


