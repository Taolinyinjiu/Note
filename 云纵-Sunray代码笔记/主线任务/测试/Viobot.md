# Viobot2
> 在线文档：https://baton-doc.readthedocs.io/en/viobot2/


## 测试内容
1. 使用viobot2原生代码，即Stereo3与Stereo4代码，测试定位稳定性
2. 部署VINS Fusion ，使用viobot2的双目信息和imu数据(已做硬件同步)


## 记录
- 更新固件包，由于viobot2中缺少更新文件夹，在指定目录创建文件夹，进行更新，以测试stereo4算法
- 更新固件包后丢失网卡驱动，重新挂载是从的
- Viobot2 编译vins卡死！
- viobot输出的里程计与动捕里程计相同，但可惜的是里程计的坐标轴为相机的坐标轴，因此需要进行坐标变换才能使用姿态信息
- viobot使用双目鱼眼，vins_fusion原生代码不支持，vins_fisheyes使用vins_gpu版本，做了基于cuda的优化，如果需要缝合的话，需要提取出对鱼眼进行的修改。或者通过畸变参数，直接从 鱼眼 -> 去畸变图像(让vins用针孔模型) -> vins 



# 草稿

## 开机自启动部分

**sunray.service** 
```bash
[Unit]
Description=Start Sunray Task

[Service]
Type=simple
User=PRR
ExecStart = /home/PRR/Sunray/General_Module/sunray_viobot_unit/SunrayTask.sh

[Install]
WantedBy = multi-user.target
```

**communication.service**
```bash
[Unit]
Description=Start communication Task

[Service]
Type=simple
User=PRR
ExecStart = /home/PRR/Sunray/server/communication.sh

[Install]
WantedBy = multi-user.target
```

**user_startup.service**
```bash
[Unit]
Description=Start User_task
Wants=network-online.target
After=network-online.target
[Service]
Type=simple
User=root
ExecStart = /etc/user_setup/user_startup.sh

[Install]
WantedBy = multi-user.target
```


### 外参矩阵信息
**/baton/camera_left_info**
fx = 166.13322688817476
fy = 165.9467389010188
cx = 319.35103726266544
cy = 240.286134330862
```bash
yundrone@PR-VIO:~$ rostopic echo /baton/camera_left_info
header: 
  seq: 29
  stamp: 
    secs: 1767954697
    nsecs: 587378118
  frame_id: ''
height: 480
width: 640
distortion_model: "ds"
D: [-0.25880036366773357, 0.5694417869803329, 0.0, 0.0, 0.0]
K: [166.13322688817476, 0.0, 319.35103726266544, 0.0, 165.9467389010188, 240.286134330862, 0.0, 0.0, 1.0]
R: [1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0]
P: [166.13322688817476, 0.0, 319.35103726266544, 0.0, 0.0, 165.9467389010188, 240.286134330862, 0.0, 0.0, 0.0, 1.0, 0.0]
binning_x: 0
binning_y: 0
roi: 
  x_offset: 0
  y_offset: 0
  height: 0
  width: 0
  do_rectify: False  
```

**/baton/camera_right_info**
fx = 165.2586695753492
fy = 165.08039770783745
cx = 320.4303155521163
cy = 240.50036809997798
```bash
yundrone@PR-VIO:~$ rostopic echo /baton/camera_right_info
header: 
  seq: 202
  stamp: 
    secs: 1768221260
    nsecs: 732915750
  frame_id: ''
height: 480
width: 640
distortion_model: "ds"
D: [-0.2637697300858231, 0.5676677977338664, 0.0, 0.0, 0.0]
K: [165.2586695753492, 0.0, 320.4303155521163, 0.0, 165.08039770783745, 240.50036809997798, 0.0, 0.0, 1.0]
R: [0.9999947436156119, 0.0025570909668320993, 0.0019934961584960973, -0.002558565058758895, 0.9999964550963484, 0.0007372513662528807, -0.0019916038729353557, -0.0007423479805922073, 0.9999977412141935]
P: [165.2586695753492, 0.0, 320.4303155521163, 0.05926505041655359, 0.0, 165.08039770783745, 240.50036809997798, -0.00019474847739676016, 0.0, 0.0, 1.0, 9.659917044528823e-05]
binning_x: 0
binning_y: 0
roi: 
  x_offset: 0
  y_offset: 0
  height: 0
  width: 0
  do_rectify: False
---
```

**/baton/CamL2Imu **

```bash
yundrone@PR-VIO:~$ rostopic echo /baton/CamL2Imu 
header: 
  seq: 676
  stamp: 
    secs: 1768221734
    nsecs: 769104758
  frame_id: ''
pose: 
  position: 
    x: 0.029186738654971123
    y: 0.004354121629148722
    z: -0.0005303110228851438
  orientation: 
    x: -0.0038853995624466165
    y: 0.9999922066623276
    z: -0.0005794557848990919
    w: 0.00038529823866041815
---
```

**/baton/CamR2Imu **
```bash
^Cyundrone@PR-VIO:~$ rostopic echo /baton/CamR2Imu 
header: 
  seq: 713
  stamp: 
    secs: 1768221771
    nsecs: 756570076
  frame_id: ''
pose: 
  position: 
    x: -0.030074915009868683
    y: 0.003698707826114168
    z: -0.0006720860447027272
  orientation: 
    x: -0.005163865204983145
    y: 0.9999864532685685
    z: -0.00021392121133001254
    w: -0.0006131492001486324
---
```


## 鱼眼相机参数

D 164.7
H 164.7
V 123.8