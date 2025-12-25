#  Sunray150安装D435i驱动

Sunray150使用机载电脑为N150,核心参数为4核4线程，功耗TDP 6w，最高睿频为3.6GHz，架构为 X86 Alder Lake

D435i结构及工作原理参考这篇文章：https://zhuanlan.zhihu.com/p/689259440

## 驱动安装

D435i的驱动包括两部分，Intel Realsense SDK2.0 和 realsense-ros，前者为D435i提供驱动支持，后者提供了ros下使用realsense深度相机的软件包

参考该链接完成Ubuntu下对ntel Realsense SDK2.0 的安装：https://github.com/realsenseai/librealsense/blob/master/doc/distribution_linux.md
(注：Jetson系列开发板参考另外的链接：https://github.com/IntelRealSense/librealsense/blob/master/doc/installation_jetson.md)
首先注册Intel服务器公钥
```bash
sudo mkdir -p /etc/apt/keyrings
curl -sSf https://librealsense.realsenseai.com/Debian/librealsense.pgp | sudo tee /etc/apt/keyrings/librealsense.pgp > /dev/null
```
将服务器添加到apt的存储库
```bash
echo "deb [signed-by=/etc/apt/keyrings/librealsense.pgp] https://librealsense.realsenseai.com/Debian/apt-repo `lsb_release -cs` main" | \
sudo tee /etc/apt/sources.list.d/librealsense.list
sudo apt-get update
```
安装需要的软件包
```bash
sudo apt-get install librealsense2-dkms
sudo apt-get install librealsense2-utils
sudo apt-get install librealsense2-dev
sudo apt-get install librealsense2-dbg
```
完成后安装与ros相关的部分realsense-ros
```bash
sudo apt install ros-<ROS_DISTRO>-librealsense2
```
在我为sunray150安装realsense-ros的时候，遇到了tsinghua作为ros软件包源无法读取的情况，这个可能有两种，一个是我使用的测试机有段时间没用，ros包的公钥过期了，另一个可能是tsinghua自身源的问题，通过换源，将ros的源改为ustc源应该可以解决这个问题。
```bash
# 首先备份原文件，注意这里应该通过cd 命令直接进入到/etc.apt/sources.list.d文件夹下查看ros源的文件名，而非直接执该命令，当然也可以通过tab补全
sudo cp /etc/apt/sources.list.d/ros-latest.list /etc/apt/sources.list.d/ros-latest.list.bak
# 修改源为ustc源,需要使用sudo的原因是该文件在/etc目录下，需要权限否则无法保存
sudo vim /etc/apt/sources.list.d/ros-latest.list
# 写入的命令为
deb https://mirrors.ustc.edu.cn/ros/ubuntu focal main
# 写入完成后需要添加ros软件包的公钥
sudo apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654 
```

完成后可以选择安装apt仓库下的realsense驱动包
```bash
sudo apt install ros-noetoc-realsense2-camera
```
## 驱动选择

在完成上述的操作后，在ros的opt库里会存在intel给的d435i默认的驱动软件包，但是这个软件包存在一个缺点，就是D435i存在一个红外IR发射器，用来加强对深度的精确检测，在面对大白墙等纹理特征缺失的场景有效估计深度，然而这个红外IR发射器，会导致双目黑白图像带有白色斑点，这是因为双目相机是通过红外来感知图像的

本次项目主要为实现基于VINS的感知定位，根据VINS项目的特性，传入的双目图像帧数保持在25-30Hz，IMU传入的频率保持在200Hz，会是一个比较理想的情况。同时realsense的驱动并非不能更改，fastlab实验室通过动态的开关IR发射器，实现了一帧图像进行双目定位感知，一帧图像用于估计深度这样的方式，显然的这会导致双目图像的频率降低，但会带来深度估计的提高。因此VINS项目中如果我们使用该驱动包，可以通过这样的方式来实现
```bash
# 首先创建一个软件包环境
mkdri -p vins_realsense/src
cd vins_realsense/src
git clone https://gitee.com/Taolinyinjiu/modified_realsense2_camera.git
cd ..
catkin build
```
值得注意的是，该软件包已经很久没有更新了，同时该软件包推荐的D435i固件版本为5.13.0.50，该固件可以在链接https://dev.realsenseai.com/docs/firmware-releases-d400下载到，通过官方工具realsense-viewer进行固件刷写，但是该仓库推荐的固件刷写教程似乎丢了，需要结合网上的资料。
目前我拿到手的D435i的固件版本应该是5.15的，比这个高了两个版本，因此我刷写到了5.13.0.50

## 驱动使用

通过下面的命令得到ros节点，在默认的官方驱动中只发布rgb图像，depth图像，在修改过得ros驱动中会发布imu话题，双目图像，深度图像和rgb图像，但是话题数量会少很多，用来节省cpu资源和带宽
```bash
roslaunch realsense2_camera rs_camera.launch 
```
注意，当USB链接线无法达到3.0时，下面的参数会导致无法发布对应的图像数据
```bash
[ WARN] [1766455070.248216700]: Given stream configuration is not supported by the device!  Stream: Depth, Stream Index: 0, Width: 640, Height: 480, FPS: 60
[ WARN] [1766455070.248333797]: Given stream configuration is not supported by the device!  Stream: Infrared, Stream Index: 1, Width: 640, Height: 480, FPS: 60
[ WARN] [1766455070.248400071]: Given stream configuration is not supported by the device!  Stream: Infrared, Stream Index: 2, Width: 640, Height: 480, FPS: 60
```
这个警告表明，fps为60，分辨率为640x480的参数，无法在USB2.0的情况下发布，如果要得到数据，只能降低FPS或者分辨率。


## 修改后的驱动存在问题

存在问题为，当ctrl+c结束该节点时，再次启动时会报错如下
```bash
[ INFO] [1766455992.418931306]: Setting Dynamic reconfig parameters.
 23/12 10:13:14,850 WARNING [140448352052992] (messenger-libusb.cpp:42) control_transfer returned error, index: 300, error: Resource temporarily unavailable, number: b
 23/12 10:13:14,904 WARNING [140448352052992] (messenger-libusb.cpp:42) control_transfer returned error, index: 300, error: Resource temporarily unavailable, number: b
```

question:当D435i插在双路电源接口时，也就是在N150原先的供电位置时，会导致[ WARN] [1766456347.169589825]: No RealSense devices were found!
怀疑是N150设计时，两个typeC口的功能设计不同，导致该口只能供电，不能做3.0？

解决方法：将供电线缆的两端对换，然后充电口线缆朝下/朝上，D435i链接到左侧的TypeC口，
影响：线缆口朝下时导致该侧电机上方气流紊乱？

