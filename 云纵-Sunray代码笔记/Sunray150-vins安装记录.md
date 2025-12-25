# Sunray150-vins安装记录

vins分为许多的版本，比如vins-mono vins-fusion vins-fusion-gpu等，由于N150并不具备CUDA核，因此只能使用CPU版本的vins，本次项目选择的算法为vins-fusion
vins-fusion仓库地址为：https://github.com/HKUST-Aerial-Robotics/VINS-Fusion

## 本体

为了简单起见，vins本该丢进Sunray主线一起编译，但是考虑到测试机上Sunray项目估计存在一些数据，因此暂时分开来弄
由于vins在提出的时候，使用的opencv版本相对于现在来说比较老了，因此它有很多的宏定义或者函数已经被更换了，这里git时选择的是我修改后的版本，只需要安装ceres求解器后就可以直接进行编译了
由于Sunray150没有配备VPN，因此这里先使用gitee仓库，顺带我把ceres也放在了这个仓库里面
```bash
# 进入之前的ros 工作空间
cd ~/Documents/GitHub/vins_realsense/src
# git 修改后的VINS,
git clone https://gitee.com/Taolinyinjiu/sunray_vins.git
# 进入仓库中的ceres求解器文件夹
cd sunray_vins/ceres_dep
# 解压
tar xzvf ceres-solver-1.14.0.tar.gz
# 进入编译
cd ceres-solver-1.14.0
# 创建编译文件夹
mkdir build
cd build
# 编译前检查依赖是否都安装了
sudo apt-get update
sudo apt-get install -y libgoogle-glog-dev libgflags-dev libatlas-base-dev libsuitesparse-dev
# 开始编译过程
cmake ..
# 注意，不要使用-j参数，会导致内存不足编译失败,使用单make 或者 make -j2，编译时间确实慢
make -j2
sudo make install
# 依赖安装完成后，进入到vins的编译，注意vins的编译过程中尽量不要开其他的程序，以免导致cpu占用过多，编译过程卡死
cd ~/Documents/GitHub/vins_realsense
# 编译的过程可能会很慢，多等等吧,注意由于N1150性能及内存的限制，使用时需要带上限制参数 -p 1 -j 2
catkin build -p 1 -j 2
```
