连接电池，启动机载电脑，通过realvnc连接无人机

打开QGC，提高imu频率，nxtpx4和cuav的都提高，后面录制的时候都录上，确定能否使用nxtpx4的，还是说nxtpx4只是外参难调了一点
cuav v6x使用这个命令
mavlink stream -d /dev/ttyACM0 -s HIGHRES_IMU -r 150
nxtpx4可以直接从mavros提高频率
``` bash
# 启动mavros
roslaunch mavros duel_px4.launch 
# 检查cuav的imu频率
rostopic hz /cuav/mavros/imu/data_raw
# 提高nxtpx4的imu频率
rosservice call /nxtpx4/mavros/set_message_interval 105 200
# 检查nxtpx4的imu频率
rostopic hz /nxtpx4/mavros/imu/data_raw
```
随后启动D435i相机，开始推流视频
```bahsr
cd ~/Documents/GitHub/vins_realsense/
source devel/setup.bash
roslaunch realsense2_camera rs_camera.launch
```
开始录制rosbag
```bash
rosbag record -o name /cuav/mavros/imu/data_raw /camera/infra1/image_rect_raw /camera/infra2/image_rect_raw 
```

