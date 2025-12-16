# sunray_msgs 消息包解读记录


## sunray_msgs/UAVState
无人机状态消息
```python
# 消息头
std_msgs/Header header
  uint32 seq
  time stamp
  string frame_id
# uav 自身id
uint8 uav_id
# uav 连接状态
bool connected
# uav 解锁状态
bool armed
# uav 当前模式
string mode
# uav 降落状态
uint8 landed_state
# uav 电池状态
float32 battery_state
# uav 电池百分比
float32 battery_percentage
# uav 定位源
uint8 location_source

bool odom_valid
# vio定位是否启动
bool vio_start
# 
string algo_status
# 位置
float32[3] position
# 速度
float32[3] velocity
# 朝向(欧拉角)
float32[3] attitude
# 四元数
geometry_msgs/Quaternion attitude_q
  float64 x
  float64 y
  float64 z
  float64 w
# 角速度
float32[3] attitude_rate
# 期望点位置
float32[3] pos_setpoint
# 期望点速度
float32[3] vel_setpoint
# 期望点角加速度
float32[3] att_setpoint
# 期望点油门
float32 thrust_setpoint
# 控制模式
uint8 control_mode
# 移动模式
uint8 move_mode
# 起飞高度
float32 takeoff_height
# 返航点位置
float32[3] home_pos
# 返航点Yaq角
float32 home_yaw
# 悬停点位置
float32[3] hover_pos
# 悬停点Yaw角
float32 hover_yaw
# 降落位置
float32[3] land_pos
# 降落Yaw点
float32 land_yaw

```

## sunray_msgs/UAVSetup

```python

# 未解锁
uint8 DISARM=0
# 解锁
uint8 ARM=1
# 设置PX4模式
uint8 SET_PX4_MODE=2
# 重启PX4
uint8 REBOOT_PX4=3
# 设置控制模式
uint8 SET_CONTROL_MODE=4
# 紧急锁定
uint8 EMERGENCY_KILL=5

uint8 INIT=0
# 遥控器输入控制
uint8 RC_CONTROL=1
# 命令控制
uint8 CMD_CONTROL=2
# 着陆控制
uint8 LAND_CONTROL=3

uint8 WITHOUT_CONTROL=4
# 消息头
std_msgs/Header header
  uint32 seq
  time stamp
  string frame_id

uint8 cmd
# px4模式
string px4_mode
# 控制模式
string control_mode

```


## sunray_msga/UAVControlCMD

```python

uint8 XyzPos=1
uint8 XyzPosYaw=4
uint8 XyzPosYawrate=5
uint8 XyzVel=2
uint8 XyzVelYaw=6
uint8 XyzVelYawrate=7
uint8 XyVelZPos=3
uint8 XyVelZPosYaw=8
uint8 XyVelZPosYawrate=9
uint8 XyzPosVelYaw=10
uint8 XyzPosVelYawrate=11
uint8 PosVelAccYaw=12
uint8 PosVelAccYawrate=13
uint8 XyzPosYawBody=14
uint8 XyzVelYawBody=15
uint8 XyVelZPosYawBody=16
uint8 GlobalPos=17
uint8 XyVelZPosYawrateBody=18
uint8 CTRL_XyzPos=50
uint8 CTRL_Traj=51
uint8 Point=30
uint8 Takeoff=100
uint8 Land=101
uint8 Hover=102
uint8 Waypoint=103
uint8 Return=104
std_msgs/Header header
  uint32 seq
  time stamp
  string frame_id
uint8 cmd
float32[3] desired_pos
float32[3] desired_vel
float32[3] desired_acc
float32[3] desired_jerk
float32[3] desired_att
float32 desired_thrust
float32 desired_yaw
float32 desired_yaw_rate
float32 latitude
float32 longitude
float32 altitude

```