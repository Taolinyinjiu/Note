1. 编译依赖包支持
```bash
# 核心编译工具
sudo apt-get install build-essential cmake unzip pkg-config

# 图像格式支持
sudo apt-get install libjpeg-dev libpng-dev libtiff-dev

# 视频处理支持
sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
sudo apt-get install libxvidcore-dev libx264-dev

# GUI 库
sudo apt-get install libgtk-3-dev

# 优化库
sudo apt-get install libatlas-base-dev gfortran

```

2. cmake配置命令
cmake -D CMAKE_BUILD_TYPE=Release \
      -D CMAKE_INSTALL_PREFIX=/usr/local \
      -D BUILD_opencv_python2=OFF \
      -D BUILD_opencv_python3=ON \
      -D WITH_CUDA=ON \
      -D WITH_CUDNN=ON \
      -D WITH_TBB=ON \
      -D OPENCV_DNN_CUDA=ON \
      -D ENABLE_FAST_MATH=1 \
      -D CUDA_FAST_MATH=1 \
      -D CUDA_ARCH_BIN="8.9" \
      -D OPENCV_EXTRA_MODULES_PATH=../../opencv_contrib/modules \
      ..