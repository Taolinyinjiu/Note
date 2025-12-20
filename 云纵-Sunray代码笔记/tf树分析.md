```bash
roslaunch sunray_simulator sunray_sim_vins.launch
```

打开vins仿真环境，模型为sunray150_mid360_d435i，世界为aws-robomaker-small-house-world，Gazebo环境为禁用gui模式

### 分析tf树

打开rqt中的tf tree，观察当前有三个tf树

- map -> map_ned
- odom -> odom_ned
- base_link -> base_link_frd

首先map为地图系，odom为里程计，base_link为机器人自身机体系，目前没有看到d435系和mid360系，因此需要进行tf变换



### D435i的TF树关系

  <model name="D435i">
    <link name="camera_link">

复盘:在sdf文件中，通过include导入的组件，可能会出现坐标系的问题，这时候需要使用tf2进行tf变换
因为include的组件，其子坐标系常为model_name::link这样的名字，此时，当使用tf而非tf2进行tf变换时，rqt并不能够读取参数，并且会出现error，但是tf2可以做到。因此后续过程中，需要学习对tf2的使用，并且是优先使用tf2

