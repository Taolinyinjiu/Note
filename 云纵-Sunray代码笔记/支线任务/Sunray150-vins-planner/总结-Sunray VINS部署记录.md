## 浅谈VINS

VINS全称为Visual Inertial Navigation System,翻译过来就是视觉惯性导航系统。虽然名字中有着导航二字，但VINS并没有像A*之类的规划算法，而是偏向于确定机器人在空间中的位置与姿态，也就是我们常说的SLAM(即时建图与同步定位)。VINS算是一个系列，VINS Mono在2019年由香港科技大学的沈劭劼老师团队 HKUST Aerial Robotics Group 提出并发表在IEEE Transactions on Robotics上，Mono是Monocular的缩写，也就是说VINS Mono是基于单目摄像头所实现的。后续又提出了VINS Fusion，Fusion算是Mono的扩展，更多的时候，我们提到VINS，其实指的是使用双目摄像头的VINS Fusion。

### VINS的优点

简单的来说，VINS = VO+IMU (Visual Odometry 视觉里程计)= VIO(Visual Inertial Odometry 视觉惯性里程计)，由于VINS引入了IMU的关系，解决了纯粹基于视觉的SLAM在快速运动，遮挡，弱纹理环境下出现漂移导致失效的问题，同时也通过视觉修正了IMU的零偏漂移。

同时，由于VINS Fusion使用了双目摄像头，因此可以获得尺度信息，在初始化阶段可以通过静止摆放对齐重力后，小幅度的移动观察里程计收敛情况。而VINS Mono则需要在初始化时大幅度的剧烈运动，来获得单目的尺度信息完成初始化，在后续飞行的过程中，也需要尽量保持运动，因此VINS Fusion会更适合用在无人机上。

### VINS的核心技术

- IMU预积分：简明预积分推导 - 半闲居士(`高翔博士`)的文章 - 知乎 https://zhuanlan.zhihu.com/p/388859808 
- IMU与积分：IMU预积分 (解闷版) - 郑纯然Range(`FAST-LIVO2作者之一`)的文章 - 知乎https://zhuanlan.zhihu.com/p/1911921324726649326
- 紧耦合的后端优化：VINS是基于优化的方法来估计机体的位姿的，VINS 使用滑动窗口（Sliding Window）滤波器，将视觉特征点和 IMU 状态放在同一个残差方程中进行非线性优化。相比松耦合，这种方式能更充分地利用传感器信息，精度更高。相应的，这也是VINS对CPU占用较高的原因，在远程桌面可视化的情况下，VINS的里程计会出现比较严重的滞后，当VINS和Ego planner同时运行时，rviz可能会无法显示出障碍物点云。
- 鲁棒的初始化：VINS提供了一套健壮的初始化程序，可以快速对其传感器坐标系
- 在线估计相机与imu之间的外参矩阵
- 闭环检测与全局优化：对于一个完整的SLAM框架来说，闭环检测与全局优化是不必可少的一部分，他可以生成全局一致的地图，但当我们将VINS作为无人机的定位源时，闭环检测与全局优化并没有意义，因为里程计是不允许产生突变的，而回环检测触发时，可以看作是有一双无形的大手把偏移的路径扯回来，因此回环检测和全局优化，主要是为建图服务的。

## 在Sunray150上部署VINS

Sunray150上的双目相机一共有两款，分别是D435i和Mini Viobot,后者类似t265，可以认为自身就有一个vio算法，插到机载电脑上就可以输出里程计，当然也可以通过ros接口读取相机的图像数据，以及板载的imu与相机之间的外参矩阵，然后实现vins算法。
简单的来说，部署vins需要的东西并不多，20-30Hz发布频率的双目图像，150-200Hz发布频率的IMU数据，双目相机与IMU之间的变换矩阵(4x4，旋转矩阵+线性xyz位置变换，填充0 0 0 1变成方阵/齐次阵方便数学运算)
 
### D435i驱动安装
假设我们使用D435i部署VINS，则需要安装D435i的驱动，这里参考另一篇文章`Sunray150-D435i驱动安装记录`

### VINS依赖与编译
关于VINS如何安装依赖Ceres求解器，以及如何在N150上顺利编译不死机，参考另一篇文章`Sunray150-vins安装记录`


### VINS调试记录

#### IMU噪声测定

这里有很多的方式来测定IMU的噪声，我提供一个python脚本，在使用前需要先安装一些依赖组件
```bash
pip install numpy PyYAML matplotlib tqdm
sudo apt-get install python3-rosbag
```
然后是这个脚本的内容
```python
#!/usr/bin/env python3
import rosbag
import numpy as np
import yaml
import os
import matplotlib.pyplot as plt
from tqdm import tqdm
import argparse

def calibrate_imu(bag_file, topic, output_dir):
    """执行IMU校准"""
    print(f"处理 {bag_file} 中的 {topic} 数据...")
    
    # 提取数据
    timestamps = []
    accel_data = []
    gyro_data = []
    
    with rosbag.Bag(bag_file, 'r') as bag:
        # 获取消息总数
        total_msgs = bag.get_message_count(topic)
        print(f"总消息数: {total_msgs}")
        
        # 遍历消息
        for _, msg, t in tqdm(bag.read_messages(topics=[topic]), total=total_msgs):
            # 存储时间戳
            timestamps.append(msg.header.stamp.to_sec())
            
            # 存储加速度数据
            accel_data.append([
                msg.linear_acceleration.x,
                msg.linear_acceleration.y,
                msg.linear_acceleration.z
            ])
            
            # 存储陀螺仪数据
            gyro_data.append([
                msg.angular_velocity.x,
                msg.angular_velocity.y,
                msg.angular_velocity.z
            ])
    
    # 转换为numpy数组
    timestamps = np.array(timestamps)
    accel_data = np.array(accel_data)
    gyro_data = np.array(gyro_data)
    
    # 计算统计量
    duration = timestamps[-1] - timestamps[0]
    accel_bias = np.mean(accel_data, axis=0)
    gyro_bias = np.mean(gyro_data, axis=0)
    accel_noise = np.std(accel_data, axis=0)
    gyro_noise = np.std(gyro_data, axis=0)
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 保存原始数据
    np.save(os.path.join(output_dir, 'timestamps.npy'), timestamps)
    np.save(os.path.join(output_dir, 'accel_data.npy'), accel_data)
    np.save(os.path.join(output_dir, 'gyro_data.npy'), gyro_data)
    
    # 生成校准报告
    generate_report(timestamps, accel_data, gyro_data, output_dir)
    
    # 生成可视化图表
    generate_plots(timestamps, accel_data, gyro_data, output_dir)
    
    print(f"校准完成! 结果保存在 {output_dir}/")

def generate_report(timestamps, accel_data, gyro_data, output_dir):
    """生成校准报告"""
    duration = timestamps[-1] - timestamps[0]
    
    report = {
        'imu_name': 'px4_imu_calibration',
        'duration_seconds': float(duration),
        'duration_minutes': float(duration/60),
        'data_points': int(len(timestamps)),
        'accel': {
            'bias_x': float(np.mean(accel_data[:, 0])),
            'bias_y': float(np.mean(accel_data[:, 1])),
            'bias_z': float(np.mean(accel_data[:, 2])),
            'noise_x': float(np.std(accel_data[:, 0])),
            'noise_y': float(np.std(accel_data[:, 1])),
            'noise_z': float(np.std(accel_data[:, 2])),
            'units': 'm/s²'
        },
        'gyro': {
            'bias_x': float(np.mean(gyro_data[:, 0])),
            'bias_y': float(np.mean(gyro_data[:, 1])),
            'bias_z': float(np.mean(gyro_data[:, 2])),
            'noise_x': float(np.std(gyro_data[:, 0])),
            'noise_y': float(np.std(gyro_data[:, 1])),
            'noise_z': float(np.std(gyro_data[:, 2])),
            'units': 'rad/s'
        }
    }
    
    # 保存YAML报告
    with open(os.path.join(output_dir, 'imu_calibration.yaml'), 'w') as f:
        yaml.dump(report, f, default_flow_style=False)
    
    # 保存文本报告
    with open(os.path.join(output_dir, 'calibration_report.txt'), 'w') as f:
        f.write("IMU校准报告\n")
        f.write("="*50 + "\n\n")
        f.write(f"数据时长: {duration:.2f}秒 ({duration/60:.2f}分钟)\n")
        f.write(f"数据点数: {len(timestamps)}\n")
        f.write(f"平均频率: {len(timestamps)/duration:.2f}Hz\n\n")
        
        f.write("加速度计统计:\n")
        f.write(f"  X轴: 偏置={report['accel']['bias_x']:.6f}, 噪声={report['accel']['noise_x']:.6f}\n")
        f.write(f"  Y轴: 偏置={report['accel']['bias_y']:.6f}, 噪声={report['accel']['noise_y']:.6f}\n")
        f.write(f"  Z轴: 偏置={report['accel']['bias_z']:.6f}, 噪声={report['accel']['noise_z']:.6f}\n\n")
        
        f.write("陀螺仪统计:\n")
        f.write(f"  X轴: 偏置={report['gyro']['bias_x']:.6f}, 噪声={report['gyro']['noise_x']:.6f}\n")
        f.write(f"  Y轴: 偏置={report['gyro']['bias_y']:.6f}, 噪声={report['gyro']['noise_y']:.6f}\n")
        f.write(f"  Z轴: 偏置={report['gyro']['bias_z']:.6f}, 噪声={report['gyro']['noise_z']:.6f}\n")

def generate_plots(timestamps, accel_data, gyro_data, output_dir):
    """生成可视化图表"""
    # 时间序列图
    plt.figure(figsize=(15, 10))
    
    # 加速度数据
    plt.subplot(2, 1, 1)
    plt.plot(timestamps - timestamps[0], accel_data[:, 0], label='Accel X')
    plt.plot(timestamps - timestamps[0], accel_data[:, 1], label='Accel Y')
    plt.plot(timestamps - timestamps[0], accel_data[:, 2], label='Accel Z')
    plt.title('加速度数据')
    plt.xlabel('时间 (秒)')
    plt.ylabel('加速度 (m/s²)')
    plt.legend()
    plt.grid(True)
    
    # 陀螺仪数据
    plt.subplot(2, 1, 2)
    plt.plot(timestamps - timestamps[0], gyro_data[:, 0], label='Gyro X')
    plt.plot(timestamps - timestamps[0], gyro_data[:, 1], label='Gyro Y')
    plt.plot(timestamps - timestamps[0], gyro_data[:, 2], label='Gyro Z')
    plt.title('陀螺仪数据')
    plt.xlabel('时间 (秒)')
    plt.ylabel('角速度 (rad/s)')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'imu_data_plot.png'), dpi=300)
    
    # 数据分布图
    plt.figure(figsize=(15, 10))
    
    # 加速度分布
    plt.subplot(2, 1, 1)
    plt.hist(accel_data[:, 0], bins=100, alpha=0.7, label='Accel X')
    plt.hist(accel_data[:, 1], bins=100, alpha=0.7, label='Accel Y')
    plt.hist(accel_data[:, 2], bins=100, alpha=0.7, label='Accel Z')
    plt.title('加速度分布')
    plt.xlabel('加速度 (m/s²)')
    plt.ylabel('频率')
    plt.legend()
    plt.grid(True)
    
    # 陀螺仪分布
    plt.subplot(2, 1, 2)
    plt.hist(gyro_data[:, 0], bins=100, alpha=0.7, label='Gyro X')
    plt.hist(gyro_data[:, 1], bins=100, alpha=0.7, label='Gyro Y')
    plt.hist(gyro_data[:, 2], bins=100, alpha=0.7, label='Gyro Z')
    plt.title('陀螺仪分布')
    plt.xlabel('角速度 (rad/s)')
    plt.ylabel('频率')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'imu_distribution.png'), dpi=300)

if __name__ == '__main__':
    # 创建参数解析器
    parser = argparse.ArgumentParser(description='IMU校准工具')
    parser.add_argument('bag_file', help='rosbag文件路径')
    parser.add_argument('--topic', default='/mavros/imu/data_raw', help='IMU话题')
    parser.add_argument('--output', default='imu_raw_results', help='输出目录')
    args = parser.parse_args()
    
    # 执行校准
    calibrate_imu(args.bag_file, args.topic, args.output)
```
这个脚本使用的方法也很简单，将无人机放平，然后使用rosbag录制至少半个小时的数据包(只需要录制imu话题就行，比如/mavros/imu/data_raw),然后修改py文件中的参数，使其符合你录制的rosbag数据包，然后运行脚本即可，等待数据分析完毕。下面是我使用nxtpx4的imu进行的校准报告
```yaml
IMU校准报告
==================================================

数据时长: 1851.04秒 (30.85分钟)
数据点数: 317188
平均频率: 171.36Hz

加速度计统计:
  X轴: 偏置=0.302433, 噪声=0.023232
  Y轴: 偏置=0.111297, 噪声=0.033951
  Z轴: 偏置=9.801075, 噪声=0.024626

陀螺仪统计:
  X轴: 偏置=-0.000015, 噪声=0.004687
  Y轴: 偏置=-0.000011, 噪声=0.003189
  Z轴: 偏置=0.000022, 噪声=0.004323
```
将参数对应填写到VINS的config配置文件中，随后就可以进入标定外参的环节。

#### 标定外参

外参，指的是相机与IMU之间的位姿变换矩阵，他包括了3x3的旋转矩阵和1x3的位移向量，以及一个凑数的行向量，组成一个4x4的齐次变换阵。与之对应的是内参，相机的内参（Intrinsic Parameters）是相机固有的内部属性，它决定了三维空间中的点如何投影到相机的二维图像平面上。简单来说，内参就像是相机的“身份证”，描述了光线进入镜头后在传感器（CCD/CMOS）上成像的几何规律。因此相机在出厂时，内参都需要进行严格的校准，对于D435i来说，部署VINS时相机的内参可以直接通过ros软件包读取相机固件参数中厂家的校准参数，不需要额外的校准。但是如果IMU使用D435i的IMU的话，则需要进行校准，因为D435i出厂时IMU并没有进行过校准，同时D435i的IMU型号为BMI055，而nxtpx4为双BMI088，虽然后者参数更好，但是对于噪声也更为敏感，对于震动较明显的情况可能效果不是很好。

标定外参的过程主要可以分为三步：
参考视频：https://www.bilibili.com/video/BV1WZ4y167me?p=11
1. 确定使用的分辨率，每个分辨率对应的相机内参都是不同的，分辨率高，细节更多，特征点也会更多，但同时会造成更大的CPU负载
2. 启动realsense软件包，以及mavros，录制相机图像，imu数据，然后在准备飞行的区域尽可能多的采集数据，绕圈走，以及将相机面向各个方向
3. 传输rosbag数据包，通常1-2分钟的数据包，大小在1-2G左右，如果录制深度图像，大小还要多上1/3，读取深度图后续可以直接测试ego是否正确生成障碍物，随后在性能相对好一些的电脑上启动vins算法，在启动前，配置文件中的外参矩阵中旋转矩阵根据情况进行粗略的标定，位移向量使用尺子或者游标卡尺进行测量，如果使用飞控的imu，则旋转矩阵可以写作$R = \begin{bmatrix} 0 & 0 & 1 \\ -1 & 0 & 0 \\ 0 & -1 & 0 \end{bmatrix}$，然后config的配置文件中，需要设置好VINS的输出日志文件夹，该文件夹下会有VINS的在线估计外参矩阵的txt文件，如果你认为这次的效果比较理想，则可以用该在线估计的矩阵替代原先估计的外参矩阵，直到里程计稳定不发散，同时里程计尺度正常。

##### Ego planner

VINS正常部署后，会输出一个稳定的里程计，对于里程计的使用有两种思路，一个是直接融合到PX4的EKF2中，作为外部里程计的输入融合，这里要解决的问题是EKF2的外部定位信息输入延时，以及PID参数的调节，主要表现在无人机移动时，外部里程计和EKF2估计的里程计之间是否会有明显的误差，在VINS的里程计尺度信息不对时，这个误差会体现的更加明显，比如EKF2跟踪外部里程计时出现明显的阻尼之类的情况。另一种方式则是将VINS与Ego Planner规划器结合起来，Ego会通过当前VINS的里程计，双目相机的深度图来获取周围的信息，接收目标点的信息，然后规划出B样条曲线。在Sunray150中，使用姿态-推力接口，pid控制器去跟踪曲线。

然而这里有一个问题，就是VINS和Ego对CPU都有一定的负载，使用nomachine会导致可视化卡死，因此这里建议使用foxglove，通过udp传递数据的方式，查看点云与发布航点，节省无人机CPU资源的同时能够正常的测试算法。

